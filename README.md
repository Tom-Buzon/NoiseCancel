# ANC Lab V0

Petit prototype Web Audio pour tester deux idées :

1. **SOURCE** — téléphone posé près de la pompe/aquarium, HP du téléphone comme anti-source.
2. **QUIET ZONE** — téléphone au point d'écoute et enceinte Bluetooth comme source secondaire.

## Le test le plus rapide

### Option A — juste tester le générateur depuis le Wi-Fi

Sur le PC/Raspberry Pi :

```bash
python serve.py
```

Le script affiche une URL du genre :

```text
http://192.168.1.42:8000
```

Ouvre-la sur le téléphone.

**Le générateur audio fonctionne en HTTP.**
En revanche, Chrome/Firefox bloquent généralement l'accès au micro sur une IP locale HTTP car `getUserMedia()` exige un contexte sécurisé.

### Option B — zéro serveur : fichier local sur le téléphone

Copie `index.html` sur le téléphone et ouvre-le localement dans un navigateur qui autorise `getUserMedia()` sur `file://`.

Le standard Web considère `file://` comme un contexte potentiellement sûr, mais le comportement concret peut varier selon le navigateur Android. Si le micro reste indisponible, utilise l'option HTTPS ci-dessous.

### Option C — Wi-Fi + micro : HTTPS local

Il faut que le certificat HTTPS soit **reconnu comme fiable par le téléphone**.

Une méthode pratique en développement est `mkcert` :

1. Installer `mkcert` sur le PC.
2. Créer/installer sa CA locale sur le PC :
   ```bash
   mkcert -install
   ```
3. Trouver l'IP Wi-Fi du PC, par exemple `192.168.1.42`.
4. Créer un certificat :
   ```bash
   mkcert -cert-file cert.pem -key-file key.pem 192.168.1.42 localhost 127.0.0.1
   ```
5. Pour que le téléphone fasse confiance à ce certificat, installer aussi la CA locale générée par `mkcert` sur le téléphone comme certificat CA utilisateur (le chemin exact dépend de la version Android).
6. Lancer :
   ```bash
   python serve.py --https cert.pem key.pem
   ```
7. Ouvrir :
   ```text
   https://192.168.1.42:8000
   ```

Si le navigateur affiche encore une erreur de certificat, **n'utilise pas le micro pour ce test tant que le certificat n'est pas réellement approuvé**.

---

## Mode 1 — téléphone sur l'aquarium

1. Déconnecte Bluetooth.
2. Pose le téléphone près de la pompe / sur la zone qui vibre, **sans bloquer le haut-parleur**.
3. Initialise le micro.
4. `Analyser 3 s`.
5. Choisis le pic dominant.
6. Coupe le micro.
7. `Jouer` à **5%**.
8. Balaye lentement la phase.
9. Ajuste finement la fréquence par ±0.01 / ±0.10 Hz.
10. Ajuste le niveau.

### Mesure correcte

Pour savoir si le bruit diminue réellement dans le salon, mesure avec :
- tes oreilles en te déplaçant ;
- idéalement un deuxième téléphone/laptop placé à 1–4 m.

Le micro du téléphone qui produit l'anti-bruit ne peut pas, à lui seul, démontrer que toute la pièce est plus calme.

---

## Mode 2 — Bluetooth / quiet zone

1. Connecte l'enceinte Bluetooth normalement dans Android.
2. Sélectionne-la comme **sortie média**.
3. Mets l'enceinte près de la position à protéger.
4. Garde le téléphone au point d'écoute.
5. Initialise le micro et analyse la pompe.
6. Lance l'anti-ton.
7. Essaie `Auto phase scan`.

Ici le micro du téléphone sert de **micro d'erreur** : le scan cherche la phase qui minimise la fréquence ciblée exactement à cet endroit.

---

## Important

- Commence à **5% de sortie**.
- La V0 limite volontairement le gain logiciel à 30%.
- Les très basses fréquences peuvent demander beaucoup d'excursion au HP d'un téléphone.
- Si le téléphone distord ou vibre fortement, baisse immédiatement le niveau.
- Le test vise d'abord les **bruits tonals et stables** : pompe, ventilateur, moteur à régime stable.
- Ne t'attends pas encore à supprimer un bruit large bande ou des claquements.

## Ce que fait la V0

- microphone Web Audio ;
- FFT 32768 points ;
- détection du pic dominant 40–1200 Hz ;
- liste de plusieurs pics ;
- interpolation du pic pour une fréquence plus précise ;
- génération d'une sinusoïde ;
- fréquence réglable au centième de Hz ;
- phase 0–359° ;
- gain 0–30% ;
- analyseur spectral ;
- auto-scan de phase expérimental.

## Limite importante

L'auto-scan mesure le résiduel **au micro du téléphone**. C'est parfait pour tester une quiet zone locale, mais pas pour optimiser automatiquement l'annulation globale à la source. Pour ça, la prochaine version devra utiliser un deuxième micro distant (ou plus tard le Raspberry Pi + plusieurs micros).
