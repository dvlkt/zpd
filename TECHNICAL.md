# Komandas argumenti

Vadošā programma izmanto Python 3 un ceļš uz galveno skriptu ir ```lib/main.py```.

| Arguments | Īsināts arguments | Apraksts |
|---|---|---|
| ```--help``` | ```-h``` | Parādīt *help* informāciju |
| ```--algorithm``` | ```-a``` | Izmantojamais algoritms (no ```/lib/algorithms``` direktorija). |
| ```--input``` | ```-i``` | Nosaukums datnēm, no kurām ielādēt datus. Ja netiks norādīts, algoritms sāks mācīties no jauna |
| ```--output``` | ```-o``` | Nosaukums datnēm, kurās tiks saglabāti dati. Ja netiks norādīts, tie netiks saglabāti |
| ```--episodes-per-hyperparameter``` | ```-eph``` | Epizožu skaits spēlē, ik pa kurai tiek nomainīti hiperparametri un restartēts algoritms (EPH jeb *Episodes per hyperparameter*) |
| ```--no-graphs``` | ```-ng``` | Nesaglabāt grafikus |
| ```--verbose``` | ```-v``` | Rādīt pilnīgi visu izvadi terminālī |

# Jaunu algoritmu pievienošana

Jaunu algoritmu var izveidot, pievienojot ```{algoritma nosaukums}.py``` failu iekšā ```/lib/algorithms```.

Šajā failā jābūt vismaz 3 funkcijām - ```init(data, load)```, ```update(data, hyperparameters)``` un ```save()```. Šīs funkcijas vislaik tiks ārēji izsauktas.

```init(data, load)``` tiek izsaukta tad, kad klients (spēle) savienojas ar serveri (AI) un nosūta svarīgāko informāciju. Līdz ar to šo funkciju var izmantot, lai uzstādītu visu algoritmu. Pirmais funkcijas arguments, ```data```, ir ```dict```, kas izskatās šādi:

```
{
    "action_count": 0, // Skaits darbībām, ko spēlē var izdarīt
    "state_size": 0 // Spēles stāvokļa parametru daudzums
}
```

Otrais funkcijas arguments, ```load```, tiek izmantots, lai ielādētu algoritma iekšējo stāvokli no kāda faila. Tā vērtība ir vai nu ```None```, ja nekāds stāvoklis netika ielādēts un algoritmam vajag sākt mācīties no sākuma, vai arī satur stāvokļa datus, kas iepriekš tika saglabāti, un tagad tos vajag atkal ielādēt.

Šajai funkcijai ir jāatgriež saraksts, kas satur trīsvietīgus kortežus. Korteža pirmais elements ir virkne, kas satur hiperparametra nosaukumu, otrais elements ir hiperparametra zemākā iespējamā vērtība un trešais elmeents ir augstākā iespējamā vērtība. Ieteicams nepārspīlēt ar minimālo un maksimālo vērtību, citādāk hiperparametru noteikšanas algoritms nestrādās ļoti labi. Piemērs:

```
[("Hiperparametrs #1", -1, 1), ("Hiperparametrs #2", 0, 5)] # Divi hiperparametri; pirmajam vērtības var būt starp -1 un 1, otrajam vērtības var būt starp 0 un 5.
```

Šim hiperparametru sarakstam var būt tehniski jebkāds garums, taču programma ņems vērā ne vairāk kā pirmos divus hiperparametrus. Līdz ar to šeit var būtībā būt norādīti 0-2 hiperparametri.

```update(data, hyperparameters)``` tiek izsaukta tad, kad klients nosūta jaunu informāciju serverim. Šī funkcija tiek izsaukta visvairāk. Funkcijas pirmais arguments, ```data```, ir ```dict```, kas izskatās šādi:

```
{
    "action_count": 0, // Skaits darbībām, ko spēlē var izdarīt
    "state_size": 0 // Spēles stāvokļa parametru daudzums
    "state": [] // Saraksts, kas satur spēles stāvokļa parametrus kā skaitļus
    "score": 0 // Pašreizējais rezultāts spēlē
    "lost": False // Vai spēle tikko tika zaudēta? (spēle gan parasti tiek nekavējoties restartēta automātiski)
}
```

```action_count``` un ```state_size``` ir pieejami ne tikai ```init``` funkcijā, bet arī šeit, taču pēc ```init``` funkcijas tie nekad nemainīsies. Tās ir būtībā konstantes. Šajai funkcijai ir jāatgriež skaitlis no -1 līdz ```action_count``` - 1, kas apzīmē darbību, kas jāizpilda spēlē.

Funkcijas otrais arguments, ```hyperparameters```, ir vai nu None, vai nu saraksts ar skaitļiem. Ja vērtība ir None, nekas īpašs nav jādara, taču ja tā nav, tad šis saraksts ir skaitļi, uz kādiem jānomaina hiperparametri, ko ```init``` funkcijā atgrieza algoritms. Tie ir doti tādā pašā secībā, kādā ```init``` funkcijā tika atgriezti. Turklāt ja ```hyperparameters``` vērtība nav None, algoritma iekšējais stāvoklis ir jārestartē. Ja algoritms nepielāgo savus hiperparametrus uz šīm vērtībām un attiecīgi arī nerestartēs savu iekšējo stāvokli, programma nestrādās pareizi.

Trešā funkcija, ```save()```, tiek izsaukta tad, kad vajag saglabāt algoritma iekšējo stāvokli. Tai nav argumentu, bet ir jāatgriež jebkāds mainīgais (parasti ```dict``` vai saraksts), kas attēlo algoritma iekšējo stāvokli.

Šeit ir piemērs vienkāršam algoritmam, kas nemācās, bet darbībām lieto skaitļus pēc nejaušas izvēles:

```
import random

def init(data, load):
	print("Šeit var iesākt darīt kaut ko...")
    return [] # Algoritmam nav hiperparametru

def update(data, hyperparameters):
	print("Atjaunojas!")
	return max(random.randint(-20, data["action_count"] - 1), -1)

def save():
	print("Saglabā visu...")
```

# Klienta un servera komunikācija

Klients (spēle) un serveris (AI) komunicē caur HTTP POST pieprasījumiem. Serveris tiek atvērts portā 1789. Klients patvaļīgi var sūtīt POST pieprasījumus, lai serverim nosūtītu jaunus datus par spēlē esošo situāciju. Šo pieprasījumu saturs ir JSON dati. Šeit ir visas īpašības, kas šajā JSON objektā var būt:

| Nosaukums | Mainīgā veids | Apraksts |
|---|---|---|
| ```title``` | ```string``` | Šī īpašība ir obligāti pirmoreiz jānosūta; pēc tam to vairs nevar nomainīt. Tas ir vienkārši spēles nosaukums. |
| ```stateSize``` | ```number``` | Šī īpašība ir obligāti pirmoreiz jānosūta. Tas ir daudzums stāvokļu parametriem, kas pēc tam tiks sūtīti |
| ```actionCount``` | ```number``` | Šī īpašība ir obligāti pirmoreiz jānosūta. Tas ir skaits darbībām, ko var spēlē izdarīt. |
| ```state``` | ```[number]``` | Skaitļu saraksts, kur katrs skaitlis ir savs parametrs stāvoklim. |
| ```score``` | ```number``` | Rezultāts spēlē. |
| ```lost``` | ```boolean``` | Apraksta, vai spēle šajā mirklī tika zaudēta. |

Jebkuru no šīm īpašībām var pieprasījumā izlaist, ja vien aprakstā nav norādīts citādāk. Serveris pēc tam atgriež atpakaļ šādu JSON objektu:

| Nosaukums | Mainīgā veids | Apraksts |
|---|---|---|
| ```action``` | ```number``` | Skaitlis no ```-1``` līdz ```actionCount - 1```, kas apzīmē darbību, kas jāizpilda spēlē. |