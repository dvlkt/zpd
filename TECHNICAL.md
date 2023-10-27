# Komandas argumenti

| Arguments | Īsināts arguments | Apraksts |
|---|---|---|
| ```--help``` | ```-h``` | Parādīt pieejamos argumentus |
| ```--port``` | ```-p``` | Ports, ko izmantot (atkarīgs no spēles) |
| ```--input``` | ```-i``` | Nosaukums datnēm, no kurām ielādēt datus. Ja netiks norādīts, algoritms sāks mācīties no jauna |
| ```--output``` | ```-o``` | Nosaukums datnēm, kurās tiks saglabāti dati. Ja netiks norādīts, tie netiks saglabāti |
| ```--episodes-per-hyperparameter``` | ```-eph``` | Epizožu skaits spēlē, ik pa kurai tiek nomainīti hiperparametri un restartēts algoritms (EPH jeb *Episodes per hyperparameter*) |
| ```--autosave-interval``` | ```-as``` | Epizožu skaits, ik pēc kurām tiek saglabāti dati. Ja netiks norādīts, dati tiks saglabāti tikai procesa apturēšanas mirklī. |
| ```--no-graphs``` | ```-ng``` | Nesaglabāt grafikus |
| ```--verbose``` | ```-v``` | Rādīt pilnīgi visu izvadi terminālī |

# Klienta un servera komunikācija

Klients (spēle) un serveris (MI) komunicē caur HTTP POST pieprasījumiem. Serveris tiek atvērts norādītajā portā. Klients patvaļīgi var sūtīt POST pieprasījumus, lai serverim nosūtītu jaunus datus par spēlē esošo situāciju. Šo pieprasījumu saturs ir JSON dati. Šeit ir visas īpašības, kas šajā JSON objektā var būt:

| Nosaukums | Mainīgā veids | Apraksts |
|---|---|---|
| ```actionCount``` | ```number``` | Šī īpašība ir obligāti pirmoreiz jānosūta. Tas ir skaits darbībām, ko var spēlē izdarīt. Pēc pirmās reizes, kad tiek atsūtīta, to vairs nevar izmainīt. |
| ```state``` | ```string``` | Virkne, kas ataino stāvokli spēlē. |
| ```score``` | ```number``` | Rezultāts spēlē. |
| ```lost``` | ```boolean``` | Apraksta, vai spēle šajā mirklī tika zaudēta. |

Jebkuru no šīm īpašībām var pieprasījumā izlaist, ja vien aprakstā nav norādīts citādāk. Serveris pēc tam atgriež atpakaļ šādu JSON objektu:

| Nosaukums | Mainīgā veids | Apraksts |
|---|---|---|
| ```action``` | ```number``` | Skaitlis no ```-1``` līdz ```actionCount - 1```, kas apzīmē darbību, kas jāizpilda spēlē. |