from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404,HttpResponseRedirect, JsonResponse
# Model classes
from .models import Profile,Projects,Rates
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Rest Framework
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
#Template loaders
from django.template.loader import render_to_string
from django.views.generic import RedirectView
from .permissions import IsAdminOrReadOnly
from .serializer import ProfileSerializer,ProjectsSerializer
from .forms import ProfileEditForm,ProjectUploadForm,VotesForm,ReviewForm
# Create your views here.


def home(request):
    projects = Projects.objects.all()
    
    context = {
        'projects':projects,
    }
    return render(request,'indexx.html',context)


def projects(request,project_id):
    try:
        projects = Projects.objects.get(id=project_id)
        all = Rates.objects.filter(project=project_id) 
        print(all)
    except Exception as e:
        raise Http404() 
    
    '''
    User count
    '''
    count = 0
    for i in all:
        count+=i.usability
        count+=i.design
        count+=i.content
    
    if count > 0:
        average = round(count/3,1)
    else:
        average = 0
        
    if request.method == 'POST':
        form = VotesForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.project = project_id
            rate.save()
        return redirect('projects',project_id)
        
    else:
        form = VotesForm() 
        
    '''
    Rating and votes logic
    '''
    votes = Rates.objects.filter(project=project_id)
    usability = []
    design = []
    content = [] 
    
    for i in votes:
        usability.append(i.usability)
        design.append(i.design)
        content.append(i.content) 
    '''
    Len() used for finding no. of items in each rating category
    '''
    if len(usability) > 0 or len(design)>0 or len(content)>0:
        average_usability = round(sum(usability)/len(usability),1) 
        average_design = round(sum(design)/len(design),1)
        average_content = round(sum(content)/len(content),1) 
            
        average_rating = round((average_content+average_design+average_usability)/3,1) 
    
    else:
        average_content=0.0
        average_design=0.0
        average_usability=0.0
        average_rating = 0.0
        
    '''
    Logic for a vote per user
    '''
    
    arr1 = []
    for use in votes:
        arr1.append(use.user_id) 
                
    auth = arr1
       
    reviews = ReviewForm(request.POST)
    if request.method == 'POST':
        
        if reviews.is_valid():
            comment = reviews.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect ('projects',project_id)
        else:
            reviews = ReviewForm()
            
       
    context = {
        'projects':projects,
        'form':form,
        'usability':average_usability,
        'design':average_design,
        'content':average_content,
        'average_rating':average_rating,
        'auth':auth,
        'all':all,
        'average':average,
        'reviews':reviews,
        
    }
    
    return render(request,'single_post.html',context) 
'''
@login_required(login_url='login')
def post_comment(request, id):
    image = get_object_or_404(Post, pk=id)
    is_liked = False
    if image.likes.filter(id=request.user.id).exists():
        is_liked = True
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            savecomment = form.save(commit=False)
            savecomment.post = image
            savecomment.user = request.user.profile
            savecomment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    params = {
        'post': post_comment,
        'form': form,
        
    }
    return render(request, 'comment.html', params)
'''
#  Check into comment instance 
'''
Getting profile for users using [Parameter : ID]
'''
@login_required
def profile(request,username):
    profile = User.objects.get(username=username)
    current_user = request.user
    
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    projects = Projects.get_profile_projects(profile.id)
    
    return render(request, 'profile.html',{"profile":profile,"profile_details":profile_details,"projects":projects}) 

@login_required(login_url='accounts/login/')
def update_profile(request):
    title = "Update Profile"
    current_user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES)
        if form.is_valid():
            home = form.save(commit=False)
            home.profile =current_user
            form.save()
        return redirect(profile)
    else:
        form = ProfileEditForm()
    context = {"current_user":current_user,"title":title,"form":form}
    return render(request, 'profile.html',context) 



'''
Uploading projects on AW3ARDS site
'''
@login_required(login_url="/accounts/login/")
def upload_project(request):
  current_user = request.user
  if request.method == 'POST':
    form = ProjectUploadForm(request.POST, request.FILES)
    if form.is_valid():
      project = form.save(commit=False)
      project.profile = request.user
      project.save()
      return HttpResponseRedirect('index.html')
  else:
    form = ProjectUploadForm()
  context = {"form":form}
  return render(request,'uploads.html',context)


class ProfileList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request,format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles,many=True)
        return Response(serializers.data)
    
    def post(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    '''
    Using serializer for (GET) projects
    '''
class ProjectsList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self,request,format=None):
        all_projects = Projects.objects.all()
        serializers = ProjectsSerializer(all_projects,many=True)
        return Response(serializers.data)
    
    def post(self, request, format=None):
        serializers = ProjectsSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    


'''
Request for user queries onsite and rendering the template to show results
'''
def search_results(request):
    if 'projects' in request.GET and request.GET['projects']:
        search_term = request.GET.get("projects")
        searched_projects = Projects.search_by_projects(search_term)
        
        message = f'{search_term}'
        
        return render(request,'search.html',{"message":message,"projects":projects})
    
    else:
        message = "You haven't searched for any term"
        return render(request,'search.html',{"message":message,"projects":projects})


















'''
@login_required(login_url='login')
def search_profile(request):
    if 'search_user' in request.GET and request.GET['search_user']:
        name = request.GET.get("search_user")
        results = Profile.search_profile(name)
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'search_.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, 'search.html', {'message': message})
'''