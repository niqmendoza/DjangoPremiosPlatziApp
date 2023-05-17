import datetime 

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.forms.models import BaseInlineFormSet
from django.contrib import admin

from .models import Question, Choice

# Create your tests here.

#testo de modelos o vistas
class QuestionModelTests(TestCase):
    def setUp(self):
        self.question = Question(question_text = "quien es el mejor cd de platzi")
    
    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        
        
        #declaro que time va a ser de ahora a 30 dias
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        
        
        #publico la pregunta y le digo al programa que sea publicado 30 dias despues de hoy con la variable time de arriba
        #future_question = Question(,pub_date=time) 
        
        
        #con assetIs me aseguro que el resultado sea falso
        self.assertIs(self.question.was_published_recently(), False)

    
    def test_was_created_recently_with_recently(self):
        time = timezone.now() - datetime.timedelta(hours=23)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)
        
    def text_was_created_recently_with_past_questions(self):
        time =timezone.now() - datetime.timedelta(days=1, minutes=1)
        self.question.pub_date=time
        self.assertIs(self.question.was_published_recently(),False)
        
        

def create_question(question_text, days):
        """
        create a question with the given "question_text", and published the given number
        of days offset to now (negative for questions published in the past,
        positive for questions that have yet to be published)
        """
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)
    
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no question exist, an apropiated message is displayed"""
        
        #hago una request http de la url de index y me guardo la respuesta
        response = self.client.get(reverse("polls:index"))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "no polls are available") #este mensaje esta en index.html
        self.assertQuerysetEqual(response.context["latest_question_list"],[])
        
    def test_future_question(self):
        """questions with a pub_date in the future aren't displayed on the index page"""
        create_question("future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "no polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])
        
    def test_past_quiestion(self):
        """
        question with a pub_date in the past are displayed on the index page
        """
        question = create_question("past question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[question])
        
        
    def test_future_question_and_past_question(self):
        """even if both past and future question exist, only past questions are displayed
        """
        past_question = question = create_question(question_text="past question",days=-30)
        future_question = question = create_question(question_text="future question",days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )
        

    def test_two_past_questions(self):
        """the question index page may display multiple questions"""
        past_question1 = question = create_question(question_text="past question 1",days=-30)
        past_question2 = question = create_question(question_text="past question 2",days=-40)
        response=self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1 , past_question2]
        )
        
    def test_two_future_questions(self):
        """The question index page may not displayed multiple questions."""
        create_question(question_text="future question 1", days=30)
        create_question(question_text="future question 2", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"],[])
        
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """the detail view of a question with a pub_date in the future returns 404 error not found"""
        future_question = create_question(question_text="future question", days= 30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """the detail view of a question with a pub_date in the past displayes the question text"""
        past_question = create_question(question_text="past question", days= -30)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
class AtLeastOneRequiredInlineFormSet(BaseInlineFormSet):

    def clean(self):
        """Check that at least one choice has been entered."""
        super(AtLeastOneRequiredInlineFormSet, self).clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
            for cleaned_data in self.cleaned_data):
            raise forms.ValidationError('At least one choice required.')


class ChoicesInline(admin.TabularInline):
    model = Choice
    formset= AtLeastOneRequiredInlineFormSet
    extra = 1
    exclude= ['votes']

class QuestionAdmin(admin.ModelAdmin):
    inlines=(ChoicesInline,)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()        
        for instance in instances:
            instance.save()            


admin.site.register(Question, QuestionAdmin)
#admin.site.register(Choice)