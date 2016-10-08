import json
from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse

from django import forms
from django.utils import timezone


from .models import Choice, Question, Picture, PictureTag

from django.core import serializers

# Index page
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    output = ', '.join([q.question_text for q in latest_question_list])
#    return HttpResponse(output)

    template = loader.get_template('app1/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


# Detail page
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, "app1/detail.html", {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'app1/results.html', {'question': question})



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'app1/detail.html', {'question':question, 'error_message':"You din't select a choice."},)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('app1:results', args=(question.id,)))



# image upload form
class ImageUploadForm(forms.Form):
    image = forms.ImageField()


def picture_create_tags(picture, tags_text):
    if tags_text == "": return

    tags = tags_text.strip().replace(' ', '_').split(',') # all space will be replaced to '_'
    for t in tags:
        picture_tag, created = PictureTag.objects.get_or_create(text=t.strip())
        picture.tags.add(picture_tag)

    return


def picupload(request):
    saved = False
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = Picture()
            m.pict = form.cleaned_data['image']
            m.upload_date = timezone.now()
            m.save()
            picture_create_tags(m, request.POST.get('tags'))
            saved = True

#    return render(request, 'app1/uploadcompleted.html', locals())
    return render(request, 'app1/picture.html', {'picture':m})


def upload(request):
    return render(request, 'app1/upload.html')


def gallery(request):
    latest_picture_list = Picture.objects.order_by('-upload_date')[:10]

    return render(request, 'app1/gallery.html', {'pictures':latest_picture_list})


def picture(request, picture_id):
    picObj = get_object_or_404(Picture, pk=picture_id)
    return render(request, 'app1/picture.html', {'picture':picObj})

def home(request):
    return render(request, 'app1/home.html')


def tag_list(request):
    tags = PictureTag.objects.all()
    return render(request, 'app1/tag_list.html', {'tags': tags})


def search_result_find_id(pictures, id):
    for i in pictures:
        if id == i['id']: return True
    return False


def search_result(request):
    query_text = request.GET.get('q')
    query_text_w_space = query_text.replace(',', ' ')
    queries = query_text.split(',')
    pictures = []

    for q in queries:
        searched_picture_list = Picture.objects.filter(tags__text=q)
        for p in searched_picture_list:
            d = {'url': p.pict.url, 'id': p.id}
            if not search_result_find_id(pictures, p.id):
                 pictures.append(d)

    return render(request, 'app1/search_result.html', {'query_text':query_text_w_space, 'pictures':pictures})


# picture_id is required as one of GET parameter
# return the serialized JSON text for array of PictureTag model-object
def api_get_picture_tags(request):
    picture_id = request.GET.get('picture_id')
    if picture_id:
        picObj = get_object_or_404(Picture, pk=picture_id)
        tags = picObj.tags.all()
        text = serializers.serialize('json', tags)

    return HttpResponse(text)

# picture_id is required as one of GET parameter
# tag_id is for removing from the picture associated with picture_id
# return the serialized JSON text for array of PictureTag model-object
def api_remove_tag_from_picture(request):
    picture_id = request.GET.get('picture_id')
    tag_id = request.GET.get('tag_id')
    if picture_id and tag_id:
        picObj = get_object_or_404(Picture, pk=picture_id)
        tags = picObj.tags.filter(pk=tag_id)
        if len(tags) > 0:
            picObj.tags.remove(tags[0])

        picObj.tags.all()
        text = serializers.serialize('json', tags)

    return HttpResponse(text)


# 'picture_id' is required as one of GET parameter
# 'tags' which has coma separated text for picture tag is also required as GET parameter
# return the serialized JSON text for array of PictureTag model-object
def api_update_picture_tags(request):
    picture_id = request.GET.get('picture_id')
    tag_text = request.GET.get('tags')
    result = 0
    if picture_id and tag_text:
        m = get_object_or_404(Picture, pk=picture_id)
        picture_create_tags(m, tag_text)
        result = 1

    return HttpResponse(result)

# Helper function for autocomplete key APIs
#
# maxCandidate means that the max number of key which is the filter results
#
# If isMulti is True, space-separated query is treated as separete keywords.
#   in this case, client code (i.e. JQuery programe) needs to handle multi query as well.
#
def helpter_api_get_picture_tags_with_term(request, isMulti, maxCandidate):
    if request.is_ajax():
        q = request.GET.get('term', '')

        if isMulti:
            # jquery sends 'something somthing2 XXX ...' if input box has separate text with 'space'
            # Hence, I'll try to get last text for searching in database!
            q2 = q.split(' ')[-1]
        else:
            q2 = q

        #        print("here!: " + q2)

        # making query for db
        tags = PictureTag.objects.filter(text__contains=q2)[:maxCandidate]
        results = []
        for tag in tags:
            tag_json = {}
            tag_json['id'] = tag.id
            tag_json['label'] = tag.text
            tag_json['value'] = tag.text
            results.append(tag_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

# single version of api_get_picture_tags_with_term
def api_get_picture_tags_with_term_1(request):
    return helpter_api_get_picture_tags_with_term(request, False, 10)

# 'term' is what Jquery adds for autocomplete key
# return the serialized JSON text for autocomplete array of 'source' object
def api_get_picture_tags_with_term(request):
    return helpter_api_get_picture_tags_with_term(request, True, 15)



