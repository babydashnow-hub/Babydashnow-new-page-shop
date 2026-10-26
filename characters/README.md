# Personnages BabyDashNow

Amara et Bibou sont dessinés entièrement en SVG par code, pour être animés dans les vidéos Monday Minute.

- `palette.js` : couleurs partagées.
- `amara.js` : `portrait(expression)`, `head(expression)`, `body()`. Expressions : calme, tendre, concentree, oups, clin, fatiguee, soulagee, fiere.
- `bibou.js` : `portrait(reaction)`, `baby(reaction)`. Réactions : fascine, boude, content, dort.
- `build-sheet.js` : génère la planche personnage.

Régénérer la planche :

```sh
node characters/build-sheet.js > characters/out/planche.html
NODE_PATH=$(npm root -g) node characters/render.js characters/out/planche.html characters/out/planche.png 1200 900
```
