from datetime import datetime
from typing import List

class Membre:
    def __init__(self, nom: str, role: str):
        self.nom = nom
        self.role = role

class Tache:
    def __init__(self, nom: str, description: str, date_debut: datetime, date_fin: datetime, responsable: Membre, statut: str):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.responsable = responsable
        self.statut = statut

class Equipe:
    def __init__(self):
        self.membres: List[Membre] = []

    def ajouter_membre(self, membre: Membre):
        self.membres.append(membre)

    def obtenir_membres(self) -> List[Membre]:
        return self.membres

class Jalon:
    def __init__(self, nom: str, date: datetime):
        self.nom = nom
        self.date = date

class Risque:
    def __init__(self, description: str, probabilite: float, impact: str):
        self.description = description
        self.probabilite = probabilite
        self.impact = impact

class Changement:
    def __init__(self, description: str, version: int):
        self.description = description
        self.version = version

class NotificationStrategy:
    def envoyer(self, message: str, destinataire: Membre):
        raise NotImplementedError

class EmailNotificationStrategy(NotificationStrategy):
    def envoyer(self, message: str, destinataire: Membre):
        print(f"Notification envoyée à {destinataire.nom} par email: {message}")

class NotificationContext:
    def __init__(self, strategy: NotificationStrategy):
        self.strategy = strategy

    def notifier(self, message: str, destinataires: List[Membre]):
        for destinataire in destinataires:
            self.strategy.envoyer(message, destinataire)

class Projet:
    def __init__(self, nom: str, description: str, date_debut: datetime, date_fin: datetime, statut: str):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.statut = statut
        self.taches: List[Tache] = []
        self.equipe = Equipe()
        self.risques: List[Risque] = []
        self.jalons: List[Jalon] = []
        self.changements: List[Changement] = []
        self.notification_context = None
        self.budget = None

    def set_notification_strategy(self, strategy: NotificationStrategy):
        self.notification_context = NotificationContext(strategy)

    def ajouter_membre_equipe(self, membre: Membre):
        self.equipe.ajouter_membre(membre)
        self.notifier(f"{membre.nom} a été ajouté à l'équipe")

    def definir_budget(self, budget: float):
        self.budget = budget
        self.notifier(f"Le budget du projet a été défini à {budget} Unité Monétaire")

    def ajouter_tache(self, tache: Tache):
        self.taches.append(tache)
        self.notifier(f"Nouvelle tâche ajoutée: {tache.nom}")

    def ajouter_risque(self, risque: Risque):
        self.risques.append(risque)
        self.notifier(f"Nouveau risque ajouté: {risque.description}")

    def ajouter_jalon(self, jalon: Jalon):
        self.jalons.append(jalon)
        self.notifier(f"Nouveau jalon ajouté: {jalon.nom}")

    def enregistrer_changement(self, description: str, version: int):
        changement = Changement(description, version)
        self.changements.append(changement)
        self.notifier(f"Changement enregistré: {description} (version {version})")

    def notifier(self, message: str):
        if self.notification_context:
            self.notification_context.notifier(message, self.equipe.obtenir_membres())

    def generer_rapport_performance(self) -> str:
        rapport = [
            "########################################",
            f"Rapport d'activités du Projet '{self.nom}':",
            f"Version: {len(self.changements)}",
            f"Dates: {self.date_debut.date()} à {self.date_fin.date()}",
            f"Budget: {self.budget or 'Non défini'} Unité Monétaire",
            "Equipe:"
        ]
        rapport.extend([f"- {membre.nom} ({membre.role})" for membre in self.equipe.obtenir_membres()])
        rapport.append("Taches:")
        rapport.extend([
            f"- {tache.nom} ({tache.date_debut.date()} à {tache.date_fin.date()}), Responsable: {tache.responsable.nom}, Statut: {tache.statut}"
            for tache in self.taches
        ])
        rapport.append("Jalons:")
        rapport.extend([f"- {jalon.nom} ({jalon.date.date()})" for jalon in self.jalons])
        rapport.append("Risques:")
        rapport.extend([
            f"- {risque.description} (Probabilité: {risque.probabilite}, Impact: {risque.impact})"
            for risque in self.risques
        ])
        rapport.append("Chemin Critique:")
        rapport.extend([
            f"- {tache.nom} ({tache.date_debut.date()} à {tache.date_fin.date()})"
            for tache in self.taches
        ])
        return "\n".join(rapport)

# Exemple d'utilisation
if __name__ == "__main__":
    membre1 = Membre("Modou", "Chef de projet")
    membre2 = Membre("Christian", "Développeur")
    projet = Projet("Nouveau Produit", "Description du projet Nouveau Produit", datetime(2024, 1, 1), datetime(2024, 12, 31), "En cours")
    projet.set_notification_strategy(EmailNotificationStrategy())
    projet.ajouter_membre_equipe(membre1)
    projet.ajouter_membre_equipe(membre2)
    projet.definir_budget(50000)
    tache1 = Tache("Analyse des besoins", "Description de l'analyse des besoins", datetime(2024, 1, 1), datetime(2024, 1, 31), membre1, "Terminée")
    tache2 = Tache("Développement", "Description du développement", datetime(2024, 2, 1), datetime(2024, 6, 30), membre2, "Non démarrée")
    projet.ajouter_tache(tache1)
    projet.ajouter_tache(tache2)
    risque = Risque("Retard de livraison", 0.3, "Élevé")
    projet.ajouter_risque(risque)
    jalon = Jalon("Phase 1 terminée", datetime(2024, 1, 31))
    projet.ajouter_jalon(jalon)
    projet.enregistrer_changement("Changement de la portée du projet", 2)
    print(projet.generer_rapport_performance())
