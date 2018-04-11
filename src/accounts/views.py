from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, FormView
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.utils.http import is_safe_url


from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail
# Create your views here.

def guest_register_view(request):
    form = GuestForm(request.POST or None)

    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next_url')
    redirect_path = next_ or next_post or None
    print ("next_post",next_post)
    print ("redirect_path", redirect_path)
    if form.is_valid():
        print (form.cleaned_data)
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")

    return redirect("/register/")


class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = 'index.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next_url')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        print ("Qaisar khan :", user)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(LoginView, self).form_invalid(form)


def user_login(request):
    username = password = ''
    response_data = {}
    print("Request ISAJAX")
    print(request.is_ajax)
    if request.POST and request.is_ajax:
        for key, value in request.POST.items():
            print("KEY:", key, " VALUE: ", value)
        username = request.POST['email']
        password = request.POST['password']
        get_user = User.objects.get(email = username)
        try:

            print ("GET USER: ", get_user)
            user = authenticate(request, username=username, password=password)
            print("USer:", user)
            if user is not None:
                print("USer Active:", user.is_active)
                print ("User: ", user)
                print ("isAuhthenticated: ", request.user.is_authenticated())

                if user.is_active:
                    login(request, user)
                    response_data = {'login' : "Success"}
                    print(response_data)
                else:
                    pass
            else:
                response_data = {'user':"password wrong"}
        except User.DoesNotExist:
            response_data = {'user':"nouser"}
    else:
        username = password = ''
        response_data = {'login': "Failed"}
    print ("OUT OF IF LOOP:", response_data)
    return HttpResponse(JsonResponse(response_data))


def login_page(request):
    form = LoginForm(request.POST or None)
    print ("Login: ", request)
    context = {
        "form": form
    }
    print ("User logged in", form.is_valid())

    next_ = request.GET.get('next')
    next_post = request.POST.get('next_url')
    redirect_path = next_ or next_post or None
    print ("next_post",next_post)
    print ("redirect_path", redirect_path)
    if form.is_valid():
        print("I am here")
        print (form.cleaned_data)
        username = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print ("User: ", user)
            print ("isAuhthenticated: ", request.user.is_authenticated())
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            print ("request.get_host:", request.get_host())
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
                #return redirect("/login")
        else:
            print("Error")

    return render(request, "accounts/login.html", context)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'


User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        form.save()
        # username = form.cleaned_data.get("username")
        # password = form.cleaned_data.get("password")
        # email = form.cleaned_data.get("email")
        # new_user = User.objects.create_user(username, password, email)
        # print ("New User: ", new_user)
    return render(request, "accounts/register.html", context)
