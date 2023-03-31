from django.shortcuts import render,redirect
from django.views import View
from .models import *
import openai
openai.api_key = "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"



class index(View):
    def get(self,request):
        request.session["member_id"]=0
        categorys=category.objects.all()
        return render(request,'index.html',{"category":categorys})
    def post(self,request):
        location=request.POST.get("location")
        locations=destination.objects.filter(category=location)
        return render(request,"places.html",{"destinations":locations})
def logout(request):
    del request.session['member_id']
    return redirect("index")
    
class places(View):
    def get(self,request):
        destinations=destination.objects.all()
        return render(request,"places.html",{"destinations":destinations})
    def post(self,request):
        destination_name=request.POST.get("destination_name")
        return render(request,"plantrip",{"destination_name":destination_name})
       
class login(View):
    def get(self,request):
        if request.session["member_id"]==0:
            return render(request,'login.html')
        else:
            return render(request,"user_profile.html")
    def post(self,request):
        mobile=request.POST.get("mobile")
        password=request.POST.get("password")
        user=profile.objects.filter(mobile=mobile).values()
        name = profile.objects.filter(mobile=mobile).values()[0]['username']
        request.session['member_id'] = mobile
        request.session["name"]=name
        if profile.objects.filter(mobile=mobile).exists():
            if user[0]["password"]==password:
                return render(request,"user_profile.html",{"name":name})
            else:
                Context={"message": "Wrong password!"}
        else:
            Context={"message": "No user found!"}
        return render(request,'login.html',Context,name)
    
class signup(View):
    def get(self,request):
        return render(request,'signup.html')
    def post(self,request):
        name=request.POST.get("name")
        mobile=request.POST.get("mobile")
        password=request.POST.get("password")
        if profile.objects.filter(mobile=mobile).exists():
            Context={"message": "User already exists with same phone number"}
        else:
            user=profile(username=name,mobile=mobile,password=password)
            user.save()
            Context={"message": "Account Successfully created!"}
        return render(request,'signup.html',Context)
    

def weather(location,date):
    import requests
    api_key = 'b9acf2ae226c44742e74ce22be917766'

    # Make a request to the OpenWeatherMap API
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}'
    response = requests.get(url)

    # Parse the response to get the daily weather forecast for the given date
    if response.status_code == 200:
        weather_data = response.json()
        daily_forecast = None
        for forecast in weather_data['list']:
            if forecast['dt_txt'].startswith(date):
                daily_forecast = forecast
                break
        if daily_forecast:
            # Extract the weather data you need from the daily_forecast dictionary
            # For example, you can get the temperature, humidity, and weather description as follows:
            temperature = daily_forecast['main']['temp']
            humidity = daily_forecast['main']['humidity']
            weather_description = daily_forecast['weather'][0]['description']
            return(f'Temperature: {temperature}, Humidity: {humidity}, Weather Description: {weather_description}')
        else:
            return(f'No daily forecast found for {date}')
    else:
        return('Error: Unable to get weather forecast')



          






class user_profile(View):
    def get(self, request, name):
        user = profile.objects.get(username=name)
        secretspots=secretspot.objects.filter(user=user)
        context = {"name": user.username,
                    "mobile": user.mobile,
                    "secretspots":secretspots
                    }
        return render(request, "user_profile.html", context)

        
def get_place(request):
    if request.method=="POST":
        destination=request.POST.get("destination")
        return render(request,"plantrip.html",{"destination":destination})
    else:
        return redirect("plantrip")

class plantrip(View):
    def get(self,request):
        if request.session["member_id"]==0:
            return render(request,'login.html')
        return render(request,'plantrip.html')
    
    def post(self,request):
        mobile=request.session['member_id']
        name = profile.objects.get(mobile=mobile)
        trip_name=request.POST.get("trip_name")
        destination_name=request.POST.get("destination")
        from_date=request.POST.get("from_date")
        duration=request.POST.get("duration")
        trip_type=request.POST.get("trip_type")
        interest=request.POST.get("interest")
        
        # Check if trip name already exists in the database
        if tripdetails.objects.filter(name=trip_name).exists():
            context = {"message": "You have already planned a trip with this name!"}
            return render(request, 'plantrip.html', context)
        
        # Generate trip itinerary using OpenAI's API
        
        prompt = "You're planning a trip to {destination} for {duration}. Create an itinerary that includes must-do activities and places to visit each day".format(destination=destination_name,duration=duration)
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        itinerary = response.choices[0].text

        
        # Send the itinerary back to the template for display
        context = {
            "trip_name": trip_name,
            "destination_name": destination_name,
            "from_date": from_date,
            "duration": duration,
            "trip_type": trip_type,
            "interest": interest,
            "itinerary": itinerary,
            "weather" : weather(destination_name,from_date),
        }
        return render(request, 'tripsuggesions.html', context)



def mytrips(request):
    mobile=request.session['member_id']
    name = profile.objects.get(mobile=mobile)
    user_trips = tripdetails.objects.filter(username=name)
    return render(request, 'mytrips.html', {'trips': user_trips})

class tripsuggestions(View):
    def get(self,request):
        if request.session["member_id"]==0:
            return render(request,'login.html')
        else:
            return render(request,'tripsuggesions.html')
    def post(self,request):
        mobile=request.session['member_id']
        name = profile.objects.get(mobile=mobile)
        trip_name=request.POST.get("trip_name")
        destination_name=request.POST.get("destination")
        from_date=request.POST.get("from_date")
        duration=request.POST.get("duration")
        trip_with=request.POST.get("trip_type")
        interests=request.POST.get("interests")
        
        trip_itinerary=request.POST.get("itinerary")
        new_trip=tripdetails(username=name,name=trip_name,
                             destination=destination_name,
                             fromdate=from_date,
                            tripwith=trip_with,duration=duration,
                            interests=interests,
      
                            trip_itinerary=trip_itinerary)
        new_trip.save()
        return redirect("mytrips")
    
def trip_advisor_api(search):
    api_key="A202233D66584E7BAD7210F46B9EB735"
    import requests

    url = f"https://api.content.tripadvisor.com/api/v1/location/search?key=A202233D66584E7BAD7210F46B9EB735&searchQuery={search}&language=en"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    return response.text


class location_review(View):
    def post(self,request):
        location=request.POST.get("location")
        img1=request.POST.get("image1")
        img2=request.POST.get("image2")
        img3=request.POST.get("image3")
        desc=request.POST.get("desc")
        rating=request.POST.get("rating")
        mobile=request.session['member_id']
        name = profile.objects.get(mobile=mobile)
        review=review_loaction(user=name,location_name=location,trip_img1=img1,trip_img2=img2,trip_img3=img3,desc=desc,rating=rating)
        review.save()
        return render(request,"location_review.html",{"message":"Review added!"})
    def get(self,request):
        return render(request,"location_review.html")
    


class secretspots(View):
    def post(self,request):
        spotname=request.POST.get("spotname")
        image=request.POST.get("image")
        desc=request.POST.get("desc")
        address=request.POST.get("address")
        location=request.POST.get("location")
        mobile=request.session['member_id']
        name = profile.objects.get(mobile=mobile)
        new_spot=secretspot(user=name,Spot_name=spotname,spot_images=image,desc=desc,location=location,address=address)
        new_spot.save()
        return render(request,"secretspot.html",{"message":"Added your secrect spot!!"})
    def get(self,request):
        return render(request,"secretspot.html")
    

class location_search(View):
    def get(self,request):
        return render(request,"search.html")
    def post(self,request):
        location=request.POST.get("location")
        return render(request,"seach.html",{"data":trip_advisor_api(location)})
