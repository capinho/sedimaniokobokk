from django.core.mail import send_mail
from templated_email import send_templated_mail
from templated_email import InlineImage
from django.contrib.auth.models import User

from .models import *


def order_created(order_id):
    """
    Envoyer un mail a l'utilisateur si la commande a bien été créée
    """
    order = Order.objects.get(id=order_id)
    subject = 'Commande effectuer avec succes'
    message = 'Chere {},\n\nVotre commande a ete enregistrer avec succes vous recevrez bientot votre commande.Votre numero de commande est {}.'.format(order.user.first_name,
                                             order.id)
#    mail_sent = send_mail(subject,
#                          message,
#                          'stagiaire-informatique@sedima.com',
#                          [order.user.email])

    with open('shop/static/img/pas_image.png', 'rb') as lena:
        image = lena.read()
    inline_image = InlineImage(filename="image", content=image)

    mail_sent= send_templated_mail(
            template_name='welcome',
            from_email='commandesedima@sedima.com',
            recipient_list=[order.user.email],
            context={
                'username':order.user.username,
                'full_name':order.user.get_full_name(),
                'signup_date':order.user.date_joined,
                #'lena_image': inline_image
            },
            # Optional:
            # cc=['cc@example.com'],
            # bcc=['bcc@example.com'],
            #headers={'SEDIMA':'SEDIMA'},
            # template_prefix="my_emails/",
            # template_suffix="email",
    )
    return mail_sent



def envoi_mail_group(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    #user = User.objects.values_list('email')
    #for a in User.objects.all():
    mail_sent= send_templated_mail(
            template_name='welcome',
            from_email='commandesedima@sedima.com',
            recipient_list=[user.email for user in User.objects.all()],
            context={
                'username':order.user.username,
                'full_name':order.user.get_full_name(),
                'signup_date':order.user.date_joined,
            },
                # Optional:
                # cc=['cc@example.com'],
                # bcc=['bcc@example.com'],
                #headers={'SEDIMA':'SEDIMA'},
                # template_prefix="my_emails/",
                # template_suffix="email",
    )
    return mail_sent
