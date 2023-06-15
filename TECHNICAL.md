# Komandas argumenti

Vadošā programma izmanto Python 3 un ceļš uz galveno skriptu ir ```lib/main.py```.

| Arguments | Īsināts arguments | Apraksts |
|---|---|---|
| ```--help``` | ```-h``` | Parādīt *help* informāciju |
| ```--algorithm``` | ```-a``` | Izmantojamais algoritms (no ```/lib/algorithms``` direktorija). |
| ```--state-input``` | ```-i``` | Ceļš uz datni, no kura ielādēt algoritma iekšējo stāvokli. Ja netiks norādīts, algoritms sāks mācīties no jauna. |
| ```--state-output``` | ```-o``` | Ceļš uz datni, kur tiks saglabāts algoritma iekšējais stāvoklis. Ja netiks norādīts, tas netiks saglabāts. |
| ```--result-output``` | ```-r``` | Ceļš uz datni, kur saglabāt algoritma rezultātus spēlē. Ja netiks norādīts, tie netiks saglabāti. |
| ```--graph-output``` | ```-g``` | Ceļš uz direktoriju, kur saglabāt Matplotlib grafikus par rezultātiem spēlē. Ja netiks norādīts, grafiki netiks izveidoti. |
| ```--no-visualization``` | ```-nv``` | Izslēgt vizualizāciju atsevišķā logā |

# Jaunu algoritmu pievienošana

Jaunu algoritmu var izveidot, pievienojot ```{algoritma nosaukums}.py``` failu iekšā ```/lib/algorithms```.

Šajā failā jābūt vismaz 3 funkcijām - ```init(data, load)```, ```update(data)``` un ```save()```. Šīs funkcijas vislaik tiks ārēji izsauktas.

```init(data, load)``` tiek izsaukta tad, kad klients (spēle) savienojas ar serveri (AI) un nosūta svarīgāko informāciju. Līdz ar to šo funkciju var izmantot, lai uzstādītu visu algoritmu. Pirmais funkcijas arguments, ```data```, ir ```dict```, kas izskatās šādi:

```
{
    "action_count": 0, // Skaits darbībām, ko spēlē var izdarīt
    "state_size": 0 // Spēles stāvokļa parametru daudzums
}
```

Otrais funkcijas arguments, ```load```, pašlaik neko nedara, bet vēlāk tiks izmantots, lai saglabātu algoritma stāvokli. Šajai funkcijai nekas nav jāatgriež.

```update(data)``` tiek izsaukta tad, kad klients nosūta jaunu informāciju serverim. Šī funkcija tiek izsaukta visvairāk. Funkcijas arguments, ```data```, ir ```dict```, kas izskatās šādi:

```
{
    "action_count": 0, // Skaits darbībām, ko spēlē var izdarīt
    "state_size": 0 // Spēles stāvokļa parametru daudzums
    "state": [] // Masīvs, kas satur spēles stāvokļa parametrus kā skaitļus
    "score": 0 // Pašreizējais rezultāts spēlē
    "lost": False // Vai spēle tikko tika zaudēta? (spēle gan parasti tiek nekavējoties restartēta automātiski)
}
```

```action_count``` un ```state_size``` ir pieejami ne tikai ```init``` funkcijā, bet arī šeit, taču pēc ```init``` funkcijas tie nekad nemainīsies. Tās ir būtībā konstantes. Šajai funkcijai ir jāatgriež skaitlis no -1 līdz ```action_count``` - 1, kas apzīmē darbību, kas jāizpilda spēlē.

Trešā funkcija, ```save()```, pašlaik neko nedara, taču vēlāk tiks izmantota datu saglabāšanai.

Šeit ir piemērs vienkāršam algoritmam, kas nemācās, bet darbībām lieto skaitļus pēc nejaušas izvēles:

```
import random

def init(data, load):
	print("Šeit var iesākt darīt kaut ko...")

def update(data):
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
| ```state``` | ```[number]``` | Skaitļu masīvs, kur katrs skaitlis ir savs parametrs stāvoklim. |
| ```score``` | ```number``` | Rezultāts spēlē. |
| ```lost``` | ```boolean``` | Apraksta, vai spēle šajā mirklī tika zaudēta. |
| ```reset``` | ```boolean``` | Ja šāda īpašība eksistē (vērtība nav svarīga), tad serverim ir jārestartē pilnīgi viss algoritms. Šo var izmantot tad, kad spēle tiek aizvērta, lai pēc tam varētu atvērt kādu jaunu spēli. |

Jebkuru no šīm īpašībām var pieprasījumā izlaist, ja vien aprakstā nav norādīts citādāk. Serveris pēc tam atgriež atpakaļ šādu JSON objektu:

| Nosaukums | Mainīgā veids | Apraksts |
|---|---|---|
| ```action``` | ```number``` | Skaitlis no ```-1``` līdz ```actionCount - 1```, kas apzīmē darbību, kas jāizpilda spēlē. |