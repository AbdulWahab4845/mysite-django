from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from .models import ContactMessage

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        ContactMessage.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            address=address
        )

        send_mail(
            subject=f'Naya Contact Message: {name}',
            message=f'Name: {name}\nEmail: {email}\nPhone: {phone_number}\nAddress: {address}',
            from_email='abdulwahab484512@gmail.com',
            recipient_list=['abdulwahab484512@gmail.com'],
            fail_silently=True,
        )

        messages.success(request, f"Shukriya {name}! Aapka message mil gaya hai.")

    return render(request, 'pages/contact.html')


def messages_list(request):
    query = request.GET.get('q', '')
    all_messages = ContactMessage.objects.all().order_by('-created_at')

    if query:
        all_messages = all_messages.filter(name__icontains=query)

    paginator = Paginator(all_messages, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/messages_list.html', {
        'page_obj': page_obj,
        'query': query,
        'total_count': all_messages.count(),
    })


def delete_message(request, message_id):
    msg = get_object_or_404(ContactMessage, id=message_id)
    msg.delete()
    messages.success(request, "Message delete ho gaya.")
    return redirect('messages_list')