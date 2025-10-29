from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact
import json


# 🏠 Home Page View
def home(request):
    return render(request, 'home.html')

# suyash/views.py
from django.shortcuts import render
from .models import Contact

def view_messages(request):
    contacts = Contact.objects.all().order_by('-created_at')  # latest first
    return render(request, 'admin_messages.html', {'contacts': contacts})



@csrf_exempt
def submit_contact(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            name = data.get('name')
            email = data.get('email')
            message = data.get('message')

            if not name or not email or not message:
                return JsonResponse({'status': 'error', 'message': 'All fields required'}, status=400)

            Contact.objects.create(name=name, email=email, message=message)

            send_mail(
                subject=f"New Contact Request from {name}",
                message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['suyashsinghbhadoria16@gmail.com'],
                fail_silently=False,
            )

            return JsonResponse({'status': 'success', 'message': 'Message sent successfully!'})

        except Exception as e:
            print("❌ Error:", e)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
