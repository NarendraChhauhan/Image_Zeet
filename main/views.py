from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ImageUploadForm
from .models import ImageUpload
from .utils import analyze_image
from django.views.decorators.csrf import csrf_exempt

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('upload_image')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('upload_image')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_upload = form.save(commit=False)
            image_upload.user = request.user
            image_upload.save()

            # Analyze the image
            details = analyze_image(image_upload.image.path)
            image_upload.details = details
            image_upload.save()
            
            return redirect('image_detail', image_id=image_upload.id)
    else:
        form = ImageUploadForm()
    return render(request, 'main/upload_image.html', {'form': form})

@login_required
def image_detail(request, image_id):
    image = ImageUpload.objects.get(id=image_id, user=request.user)
    return render(request, 'main/image_detail.html', {'image': image})

# image_app/views.py
# from django.shortcuts import render, redirect
# from django.views import View
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from .forms import UserRegistrationForm, ImageUploadForm
# from .models import ProcessedImage

# from .services import ImageProcessingService

# class SignupView(View):
#     def get(self, request):
#         form = UserRegistrationForm()
#         return render(request, 'signup.html', {'form': form})

#     def post(self, request):
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()  # Save the user in the database
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)  # Log the user in after signup
#             return redirect('upload_image')
#         return render(request, 'signup.html', {'form': form})


# class LoginView(View):
#     def get(self, request):
#         form = AuthenticationForm()
#         return render(request, 'login.html', {'form': form})

#     def post(self, request):
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             login(request, form.get_user())  # Log the user in
#             return redirect('upload_image')
#         return render(request, 'login.html', {'form': form})


# class LogoutView(View):
#     def get(self, request):
#         logout(request)  # Log the user out
#         return redirect('login')  # Redirect to login page


# @method_decorator(login_required, name='dispatch')
# class ImageUploadView(View):
#     service = ImageProcessingService()  # Use the service to process images

#     def get(self, request):
#         form = ImageUploadForm()
#         return render(request, 'upload_image.html', {'form': form})

#     def post(self, request):
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded_image = form.save(commit=False)
#             uploaded_image.user = request.user
#             uploaded_image.save()

#             # Simulate processing the image with the service
#             labels = self.service.process_image(uploaded_image.image)
#             description = self.service.extract_description(labels)

#             # Save the processed description
#             uploaded_image.description = description
#             uploaded_image.save()

#             return redirect('image_details', image_id=uploaded_image.id)
#         return render(request, 'upload_image.html', {'form': form})


# @method_decorator(login_required, name='dispatch')
# class ImageDetailsView(View):
#     def get(self, request, image_id):
#         uploaded_image = ProcessedImage.objects.get(id=image_id, user=request.user)
#         return render(request, 'image_details.html', {'uploaded_image': uploaded_image})




