import os
import django


#DODAVANJE GRADOVA U BAZU
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obrok_ba.settings')
django.setup()

from obrok.models import City

cities_list = [
    'Banovići', 'Banja Luka', 'Bihać', 'Bijeljina', 'Bosanska Krupa', 'Bosanska Otoka', 'Bratunac', 
    'Brčko', 'Bugojno', 'Busovača', 'Bužim', 'Cazin', 'Čapljina', 'Čelić', 'Čelinac', 'Čitluk', 'Derventa', 
    'Doboj', 'Doboj Istok', 'Donji Vakuf', 'Drvar', 'Foča', 'Fojnica', 'Gacko', 'Glamoč', 'Goražde', 
    'Gornji Vakuf-Uskoplje', 'Gračanica', 'Gradačac', 'Grude', 'Hadžići', 'Ilidža', 'Ilijaš', 
    'Istočna Ilidža', 'Istočni Drvar', 'Istočni Mostar', 'Jablanica', 'Jajce', 'Kakanj', 'Kalesija', 
    'Kalnik', 'Kiseljak', 'Kladanj', 'Ključ', 'Kneževo', 'Konjic', 'Kostajnica', 'Kotor Varoš', 
    'Kozarska Dubica', 'Kreševo', 'Krupa na Uni', 'Krupanj', 'Kupres', 'Laktaši', 'Livno', 'Ljubinje', 
    'Ljubuški', 'Lopare', 'Lukavac', 'Maglaj', 'Milići', 'Modriča', 'Mostar', 'Mrkonjić Grad', 'Neum', 
    'Nevesinje', 'Novi Grad', 'Novi Travnik', 'Novo Sarajevo', 'Olovo', 'Općina Centar', 'Orašje', 
    'Osmaci', 'Oštra Luka', 'Pale', 'Posušje', 'Prijedor', 'Prnjavor', 'Prozor-Rama', 'Ravno', 'Ribnik', 
    'Rogatica', 'Rudo', 'Šamac', 'Sanski Most', 'Sarajevo', 'Šekovići', 'Šipovo', 'Sokolac', 'Šolakovići', 
    'Srbac', 'Stari Grad', 'Štitar', 'Šujica', 'Šušanj', 'Šuto Orizari', 'Svornik', 'Teočak', 'Teslić', 
    'Tešanj', 'Tomislavgrad', 'Travnik', 'Trebinje', 'Tuzla', 'Ugljevik', 'Usora', 'Ustiprača', 'Vareš', 
    'Velika Kladuša', 'Velika Obarska', 'Visoko', 'Višegrad', 'Vitez', 'Vlasenica', 'Vogošća', 'Vukosavlje', 
    'Zavidovići', 'Zenica', 'Žepče', 'Živinice', 'Zvornik'
]



for city_name in cities_list:
    city, created = City.objects.get_or_create(name=city_name)
    if created:
        print(f'Dodat grad: {city_name}')
    else:
        print(f'Grad "{city_name}" već postoji u bazi podataka.')
