# NoiseCancel V1 -- Edit : Résultats peu probant

## Workflow

1. Ouvre le site près de la pompe.
2. Initialise le micro.
3. Capture 10 secondes.
4. Le profil est sauvegardé dans le stockage local du navigateur.
5. Place l'enceinte Bluetooth au plus près de la pompe.
6. Connecte-la comme sortie média Android.
7. Prends le téléphone avec toi au canapé.
8. Charge le profil.
9. Lance d'abord uniquement la fréquence dominante.
10. Balaye la phase, puis la fréquence fine, puis le volume.
11. Quand tu entends un minimum, appuie sur « Garder maintenant ».

## Important

La V1 ne rejoue pas le WAV inversé. Une capture audio faite à un instant donné perdrait sa relation de phase avec la pompe lorsque tu la rejoues plus tard. La V1 extrait les fréquences stables et les recrée avec un oscillateur dont on règle la phase.

La fréquence extraite par la FFT reste une estimation. Le balayage fin ±0,5 Hz est là pour corriger cette estimation et compenser les petites différences d'horloge.


