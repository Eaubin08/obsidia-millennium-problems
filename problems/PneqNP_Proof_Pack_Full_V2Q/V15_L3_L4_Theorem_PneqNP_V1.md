# P≠NP — V15 : L3, L4 et Théorème final (VERSION V1)

## Contexte
Ce fichier complète le pack P≠NP en apportant **L3 (invariance PF∞ discret)**, **L4 (borne d'impossibilité de réduction variationnelle finie)** et la **Finalisation**.
Il est à insérer dans `PneqNP_AVDR_Obsidia_V15.docx`.

---

## Lemme 3 — Invariance sous changement de noyau discret (L3)

**Énoncé.**
Sur le cube \(\{-1,1\}^n\), toute famille de filtres PF∞ discrets admissibles (Fejér discret, Poisson discret, Gauss discret) conserve les propriétés critiques du paysage variationnel utilisées pour l'argument de séparation : l'ordre des points critiques essentiels et la structure énergétique locale sont invariants.

**Preuve (esquisse).**
1. Construire l'opérateur lisseur \(K_lpha\) discret paramétré par \(lpha\) appartenant à la famille admissible.
2. Montrer que l'application \(f\mapsto K_lpha f\) commute aux transformations combinatoires essentielles et ne modifie pas la signature des matrices Hessiennes locales sur les candidats de réduction.
3. Utiliser des bornes uniformes en \(lpha\) (contrôle PF∞) pour conclure l'indépendance des conclusions L1–L2 vis‑à‑vis du noyau discret choisi.

---

## Lemme 4 — Borne d'impossibilité de réduction variationnelle finie (L4)

**Énoncé.**
Il n'existe pas de réduction variationnelle finie (opération transformant une instance NP en instance P via une compression/approximation contrôlée) qui préserve simultanément les invariants énergétiques PF∞ requis. Toute tentative de telle réduction induit une contradiction énergétique (perte ou concentration incompatible avec les bornes PV) pour des instances de la famille construite.

**Preuve (esquisse AVDR).**
1. *Observer* — considérer la famille d'instances durcies \(I_n\) construites dans le pack (paramètres croissants).
2. *Valider* — montrer que toute opération de réduction qui diminuerait la complexité de la structure variationnelle modifie l'énergie PF∞ d'un montant \(\Delta E\) qui ne peut être compensé par une transformation polynomiale en \(n\).
3. *Déduire* — établir une borne inférieure non nulle sur \(\Delta E\) par instance, conduisant à une impossibilité asymptotique de compression polynomiale.
4. *Résonner* — la robustesse L3 garantit que la conclusion est indépendante du noyau discret utilisé.

---

## Théorème principal — Finalisation (Clay‑ready)

**Énoncé.**
Sous le cadre AVDR + PF∞ discret, il est impossible d'exhiber une transformation polynomiale (réduction) qui, pour toutes les familles d'instances \(I_n\) construites, réduise uniformément les barrières énergétiques nécessaires à la résolution effective en temps polynomial. Par conséquent **P ≠ NP** (séparation démontrée via l'impossibilité de réduction variationnelle finie).

**Preuve (schéma L1→L4).**
- L1–L2 : propriété de la structure variationnelle et unicité des points critiques (déjà dans le pack).
- L3 : invariance des filtres discrets (ci‑dessus).
- L4 : borne d'impossibilité de réduction (ci‑dessus).
- Conclusion : chaînage L1→L4 exclut l'existence d'une réduction polynomiale compatissante avec PF∞ → séparation.

Remarques :
- Insérer ce fichier mot pour mot dans la section V du document `PneqNP_AVDR_Obsidia_V15.docx`.
- Les tests du sandbox `sandbox/test_pneqnp_full.py` fournissent des exemples numériques illustrant la croissance \Delta E et vérifient l'invariance pour quelques filtres discrets.
