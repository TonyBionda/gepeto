from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .utils import predict_from_model, get_date_dataframe


def index(request):
    return render(request, 'index.html')


# API /predict with POST method
@csrf_exempt
def predict(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required.'})
    try:
        # Get the data from POST request body.
        # date, fullMoon, vacation, match, alert
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        # Get date from the body
        date = body['date']
        # Get date dataframe
        df = get_date_dataframe(date)
        print(df)
        # Get the day of week from the dataframe
        day_of_week = df['DayOfWeek']
        # Get the fullMoon from the dataframe
        full_moon = df['IsFullMoon']
        # Get the vacation from the dataframe
        vacation = df['IsHoliday']
        # Get the match from the body
        match = body['match']
        # Get the alert from the body
        alert = body['alert']
        # Get the prediction from the model
        prediction = predict_from_model(full_moon, vacation, match, day_of_week, alert)
        # Return the prediction as JSON
        return JsonResponse({
            'prediction': prediction,
            'success': True
        })
    except Exception as e:
        return JsonResponse({'error': str(e), 'success': False})
    except KeyError as e:
        return JsonResponse({'error': str(e), 'success': False})
