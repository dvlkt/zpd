<div align="center">
    <h1>Hiperparametru ietekme uz Q mācīšanos videospēļu vidē</h1>
    <h3>Zinātniskās pētniecības darbs informātikas/programmēšanas sekcijā</h3>
</div>

**Darba autori:** Dāvis Lektauers, Kazimirs Kārlis Brakovskis

**Darba vadītāja:** Mg. sr. soc. Agnese Kramēna-Juzova

***

## Mašīnmācīšanās programma (```/lib/```)

Lai jebkura no šajā projektā pieejamajām spēlēm strādātu, fonā ir jābūt aktīvai mašīnmācīšanās programmai. Lai to paveiktu, atveriet ```lib```, izmantojot Python  interpretētāju (vismaz Python 3.10). Visus argumentus var apskatīt ```TECHNICAL.md``` vai ar ```--help``` argumentu. Pārliecinieties, ka jums ir ielādētas visas pakotnes, kas ievietotas ```requirements.txt```.

## *Google Chrome* dinozaura spēle (```/chrome-dino/```)

Lai to spēlētu, atveriet ```/chrome-dino/index.html``` interneta pārlūkprogrammā. Izmantojamais ports: ```1781```.

## *Pong* spēles atdarinājums (```/pong/```)

Lai to spēlētu, atveriet ```/pong/main.py``` ar Python 3 interpretētāju. Izmantojamais ports: ```1782```.

## *Tetris* spēles *GameBoy* versija (```/tetris/```) - pagaidām nestrādā

Lai to spēlētu, atveriet ```/tetris/main.py``` ar Python 3 interpretētāju. Izmantojamais ports: ```1783```.

Ja emulators nestrādā uz Linux platformām, var mēģināt ielādēt ```libosmesa6``` pakotni uz Debian balstītām sistēmām vai ```lib32-mesa``` / ```mesa``` uz Arch balstītām sistēmām, tad palaist komandu ```export PYOPENGL_PLATFORM=osmesa```. Ja vēl joprojām nestrādā, tad 🤷.

## *Pacman* spēles atdarinājums (```/pacman/```) - pagaidām nestrādā

Balstīts uz [raybishal/PAC-MAN](https://github.com/raybishal/PAC-MAN/tree/main) projektu.

Lai to spēlētu, atveriet ```/pacman/index.html``` interneta pārlūkprogrammā. Izmantojamais ports: ```1784```.

***

Vairāk koda paskaidrojumiem un pamācībām skatīt ```TECHNICAL.md```.

© 2022-2023, Dāvis Lektauers un Kazimirs Kārlis Brakovskis