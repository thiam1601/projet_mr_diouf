import unittest
from datetime import datetime
from app import Membre, Tache, Equipe, Jalon, Risque, Changement, NotificationContext, EmailNotificationStrategy, \
    Projet


class TestProjet(unittest.TestCase):

    def setUp(self):
        self.membre1 = Membre("Modou", "Chef de projet")
        self.membre2 = Membre("Christian", "Développeur")
        self.projet = Projet("Nouveau Produit", "Description du projet Nouveau Produit", datetime(2024, 1, 1),
                             datetime(2024, 12, 31), "En cours")
        self.projet.set_notification_strategy(EmailNotificationStrategy())
        self.tache1 = Tache("Analyse des besoins", "Description de l'analyse des besoins", datetime(2024, 1, 1),
                            datetime(2024, 1, 31), self.membre1, "Terminée")
        self.tache2 = Tache("Développement", "Description du développement", datetime(2024, 2, 1),
                            datetime(2024, 6, 30), self.membre2, "Non démarrée")
        self.risque = Risque("Retard de livraison", 0.3, "Élevé")
        self.jalon = Jalon("Phase 1 terminée", datetime(2024, 1, 31))

    def test_ajouter_membre_equipe(self):
        self.projet.ajouter_membre_equipe(self.membre1)
        self.projet.ajouter_membre_equipe(self.membre2)
        self.assertIn(self.membre1, self.projet.equipe.obtenir_membres())
        self.assertIn(self.membre2, self.projet.equipe.obtenir_membres())

    def test_definir_budget(self):
        self.projet.definir_budget(50000)
        self.assertEqual(self.projet.budget, 50000)

    def test_ajouter_tache(self):
        self.projet.ajouter_tache(self.tache1)
        self.projet.ajouter_tache(self.tache2)
        self.assertIn(self.tache1, self.projet.taches)
        self.assertIn(self.tache2, self.projet.taches)

    def test_ajouter_risque(self):
        self.projet.ajouter_risque(self.risque)
        self.assertIn(self.risque, self.projet.risques)

    def test_ajouter_jalon(self):
        self.projet.ajouter_jalon(self.jalon)
        self.assertIn(self.jalon, self.projet.jalons)

    def test_enregistrer_changement(self):
        self.projet.enregistrer_changement("Changement de la portée du projet", 2)
        self.assertEqual(len(self.projet.changements), 1)
        self.assertEqual(self.projet.changements[0].description, "Changement de la portée du projet")
        self.assertEqual(self.projet.changements[0].version, 2)


if __name__ == "__main__":
    unittest.main()
