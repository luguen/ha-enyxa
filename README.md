# ENYXA Home Assistant v0.2.2

Cette version ajoute les ressources graphiques locales de l’intégration, conformément à Home Assistant 2026.3+.

## Changements
- Images PNG dans `custom_components/enyxa/brand/`.
- Version du manifeste : `0.2.2`.
- Code fonctionnel des capteurs et de la configuration conservé depuis v0.2.1.

## Publication HACS
Copier le contenu de cette archive à la racine du dépôt `luguen/ha-enyxa`, puis commit, push et publier le tag/release `v0.2.2`.
Dans HACS, mettre à jour ENYXA puis redémarrer Home Assistant. Si le logo ne s'affiche pas immédiatement, actualiser la page et patienter pendant le rafraîchissement du cache.

Ne pas supprimer l'intégration depuis Appareils et services : la configuration et les entités existantes doivent être conservées.

Documentation : https://contributors.home-assistant.io/blog/2026/02/24/brands-proxy-api/
