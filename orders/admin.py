from django.contrib import admin
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth.admin import UserAdmin
import csv,xlwt
from django import forms
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.hashers import make_password
from import_export import resources, fields
from import_export.widgets import ManyToManyWidget

from django.http import HttpResponse
import datetime
from datetime import date

from .models import *



class UserResource(resources.ModelResource):

    groups = fields.Field(
        column_name='group_name',
        attribute='groups',
        widget=ManyToManyWidget(Group, ',','name')
    )
    def before_import_row(self,row, **kwargs):
        value = row['password']
        row['password'] = make_password(value)
    class Meta:
        model = User

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

@admin.register(Site)
class Site(ImportExportModelAdmin):
    list_display = ('nom',)


def export_commande(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="commandes.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Commande',cell_overwrite_ok=True)

    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Numero Commande','Matricule','Nom','Prenom', 'Prix', 'Quantité', 'Produits','Categories']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    commandes = queryset.values_list('order','order__user__profile__matricule','order__user__first_name','order__user__last_name', 'price', 'quantity', 'product__name','product__category__name','order__user__profile__site')
    for commande in commandes:
        row_num += 1
        for col_num in range(len(commande)):
            ws.write(row_num, col_num, commande[col_num], font_style)
    wb.save(response)
    queryset.update(status='t')
    return response

    def get_paid(self, instance):
        return instance.order.paid
export_commande.short_description = 'Exporter vers excel'

def export_commande_adv(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="commandes.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    todayDate = datetime.date.today()
    current_day = todayDate.day
    ws = wb.add_sheet('Commande',cell_overwrite_ok=True)

    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Matricule','Nom','Prenom','Quantité', 'Produits','Categories']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    commandes = queryset.values_list('order__user__profile__matricule','order__user__first_name','order__user__last_name','quantity', 'product__name','product__category__name')
    for commande in commandes:
        row_num += 1
        for col_num in range(len(commande)):
            ws.write(row_num, col_num, commande[col_num], font_style)
    wb.save(response)
    return response
export_commande_adv.short_description = 'Exporter vers excel'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    actions = [export_commande,]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id','product','price','quantity','get_nom','get_matricule','status']
    list_filter = [('order__created', DateRangeFilter), ('order__updated', DateTimeRangeFilter),]

    actions = [export_commande,export_commande_adv]
    search_fields=['price','product__name','order__user__first_name','order__user__last_name','order__user__profile__matricule']
    #list_display = ['id','price', 'quantity','user_id', 'product_id']
    #list_filter = ['order__created', 'order__updated']

    def get_actions(self, request):
        group = Group.objects.filter(user=request.user,name='adv')
        actions = super().get_actions(request)
        if group:
            if 'export_commande_adv' in actions:
                actions['export_commande_adv']
                del actions['export_commande']
                del actions['delete_selected']
            return actions
        else:
            del actions['export_commande_adv']
        return actions

    def get_list_display(self, request):
        group = Group.objects.filter(user=request.user,name='adv')
        list_display = super().get_list_display(request)
        if group:
            list_display = ['id','product','quantity','get_nom','status']
        return list_display



    def has_add_permission(self, request):
        return True

    def get_nom(self, instance):
        return '%s %s' % (instance.order.user.first_name,instance.order.user.last_name)

    def get_matricule(self, instance):
        return instance.order.user.profile.matricule

    get_matricule.short_description = 'Matricule'
    get_nom.short_description = 'Nom'


#class DateForm(forms.ModelForm):
#    class Meta:
#        model = datedispo
#        fields = ['datedebut','datefin']

#    def clean(self):
#        start_date = self.cleaned_data.get('datedebut')
#        end_date = self.cleaned_data.get('datefin')
#        if start_date > end_date:
#            raise forms.ValidationError("La date de fin des commmandes ne peut pas être inferieur à la date de debut")
#        return self.cleaned_data

#class datedispoAdmin(admin.ModelAdmin):
#    form = DateForm
#    list_display = ['datedebut','datefin']

#    def has_add_permission(self, request):
#        return True

class OrderAdmin(admin.ModelAdmin):
    list_display = ['Commande','get_nom','get_matricule']
    #list_filter = ['paid', 'created', 'updated']
    list_filter = ['created',]
    inlines = [OrderItemInline]
    search_fields = ["user__username","user__profile__matricule","user__first_name","user__last_name"]
    date_hierarchy = 'created'


    def has_add_permission(self, request):
        return False

    def Commande (self,instance):
        return instance.id

    def get_matricule(self, instance):
        return instance.order.user.profile.matricule

    def get_nom(self, instance):
        return '%s %s' % (instance.user.first_name,instance.user.last_name)
    get_nom.short_description = 'Nom'

    def get_matricule(self, instance):
        return instance.user.profile.matricule
    get_matricule.short_description = 'Matricule'


class CustomUserAdmin(UserAdmin,ImportExportModelAdmin):
    inlines = [ProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_site')
    resource_class = UserResource

    def get_site(self, instance):
        return instance.profile.site
    get_site.short_description = 'Localisation'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)





admin.site.register(OrderItem, OrderItemAdmin)
#admin.site.register(datedispo, datedispoAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Order,OrderAdmin)
