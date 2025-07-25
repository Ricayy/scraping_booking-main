import csv
import unittest

from path.root_path import root_path


class MyTestCase(unittest.TestCase):
    """
    siren
    siret
    dateCreationEtablissement
    trancheEffectifsEtablissement
    activitéPricipaleRegistreMetiersEtablissement
    etablissementSiege
    categorieJuridiqueUniteLegale
    denominationUniteLegale
    denominationUssuelleUniteLegale
    sexeUniteLegale
    nomUniteLegale
    nomUsageUniteLegale
    prenom(1-4)UniteLegale
    activitePrincipaleEtablissement
    trancheEffectifsUniteLegale
    complementAdresseEtablissement
    numeroVoieEtablissement
    indiceRepetitionEtablissement
    typeVoieEtablissement
    libelleVoieEtablissement
    codePostalEtablissement
    libelleCommuneEtablissement
    codexCedexEtablissement
    libelleCodexEtablissement
    enseigne(1-3)Etablissement
    denominationUsuelleEtablissement
    """
    default = ""
    fieldsnames_merge = [
        "id",
        "id_respartner",
        "siren",
        "siret",
        "dateCreationEtablissement",
        "trancheEffectifsEtablissement",
        "activitePrincipaleRegistreMetiersEtablissement",
        "etablissementSiege",
        "categorieJuridiqueUniteLegale",
        "denominationUniteLegale",
        "sexeUniteLegale",
        "nomUniteLegale",
        "nomUsageUniteLegale",
        "prenomUniteLegale",
        "activitePrincipaleEtablissement",
        "trancheEffectifsUniteLegale",
        "complementAdresseEtablissement",
        "adresseEtablissement",
        "libelleCommuneEtablissement",
        "codePostalEtablissement",
        "codeCedexEtablissement",
        "libelleCedexEtablissement",
        "nomRespartner",
        "enseigneEtablissement",
        "denominationUsuelleEtablissement",
        "email",
        "phone",
        "activity_ids",
        "country_id",
        "user_id",
        "is_company",
        "partner_gid",
        "company_registry",
        "company_name",
        "company_id",
        "comment",
        "street2",
        "industry_id",
        "parent_id",
        "ref_company_ids",
        "category_id",
        "company_type",
        "mobile",
        "phone_mobile_search"
    ]

    def test_merge_siren_res_partner(self):
        with open(root_path + "/test/test_siren/merge_siren_respartner.csv", "w", encoding="utf8",
                  newline="") as merge_file:
            writer = csv.DictWriter(merge_file, fieldnames=self.fieldsnames_merge)
            writer.writeheader()
        with open(root_path + "/res_partner/res_partner_to_merge.csv", "r", encoding="utf8") as res_partner_file:
            res_partner_reader = csv.DictReader(res_partner_file)
            for res_row in res_partner_reader:
                res_id = res_row["id"].replace("__export__.res_partner_", "").split("_")
                res_id = res_id[0]
                siren = self.default
                siret = self.default
                dateCreationEtablissement = self.default
                trancheEffectifsEtablissement = self.default
                activitePrincipaleRegistreMetiersEtablissement = self.default
                etablissementSiege = self.default
                categorieJuridiqueUniteLegale = self.default
                denominationUniteLegale = self.default
                sexeUniteLegale = self.default
                nomUniteLegale = self.default
                nomUsageUniteLegale = self.default
                prenomUniteLegale = self.default
                activitePrincipaleEtablissement = self.default
                trancheEffectifsUniteLegale = self.default
                complementAdresseEtablissement = self.default
                codeCedexEtablissement = self.default
                libelleCedexEtablissement = self.default
                enseigne = self.default
                denominationUsuelleEtablissement = self.default
                adresse = res_row["street"]
                libelleCommuneEtablissement = res_row["city"]
                codePostalEtablissement = res_row["zip"]
                res_name = res_row["name"]
                res_emails = res_row["email"]
                res_phone = res_row["phone"]
                activity_ids = res_row["activity_ids"]
                country_id = res_row["country_id"]
                user_id = res_row["user_id"]
                is_company = res_row["is_company"]
                partner_gid = res_row["partner_gid"]
                company_registry = res_row["company_registry"]
                company_name = res_row["company_name"]
                company_id = res_row["company_id"]
                comment = res_row["comment"]
                street2 = res_row["street2"]
                industry_id = res_row["industry_id"]
                parent_id = res_row["parent_id"]
                ref_company_ids = res_row["ref_company_ids"]
                category_id = res_row["category_id"]
                company_type = res_row["company_type"]
                mobile = res_row["mobile"]
                phone_mobile_search = res_row["phone_mobile_search"]

                res_vat = res_row["vat"].replace(" ", "")
                if "FR" in res_vat:
                    temp = ""
                    for i in range(4):
                        if i < 4:
                            temp += res_vat[i]
                    res_siren = res_vat.replace(temp, "")
                    with open(root_path + "/siren/siren_to_merge.csv", "r", encoding="utf8") as siren_file:
                        siren_reader = csv.DictReader(siren_file)
                        for siren_row in siren_reader:
                            if res_siren == siren_row["siren"]:
                                siren_ville = siren_row["libelleCommuneEtablissement"].strip()
                                if "PARIS " in siren_ville:
                                    siren_ville = siren_ville.split(" ")
                                    siren_ville = siren_ville[0]
                                type_voie_mapping = {
                                    "": self.default,
                                    "ALL": "ALLEE",
                                    "AV": "AVENUE",
                                    "BD": "BOULEVARD",
                                    "CAMI": "CHEMIN",
                                    "CAR": "CARREFOUR",
                                    "CITE": "CITE",
                                    "CHE": "CHEMIN",
                                    "CHEM": "CHEMIN",
                                    "CHS": "CHAUSSEE",
                                    "CLOS": "CLOS",
                                    "COR": self.default,
                                    "COUR": "COUR",
                                    "COTE": "COTE",
                                    "CRS": "COURS",
                                    "DOM": "DOMAINE",
                                    "ESP": "ESPLANADE",
                                    "FG": "FAUBOURG",
                                    "GR": "GRANDE RUE",
                                    "HAM": "HAMEAU",
                                    "IMP": "IMPASSE",
                                    "LD": "LIEU-DIT",
                                    "LOT": "LOTISSEMENT",
                                    "MTE": self.default,
                                    "PAS": "PASSAGE",
                                    "PARC": "PARC",
                                    "PL": "PLACE",
                                    "PLT": self.default,
                                    "PLN": "PLAINE",
                                    "PONT": "PONT",
                                    "PORT": "PORT",
                                    "PRO": "PROMENADE",
                                    "PRV": self.default,
                                    "QUA": "QUARTIER",
                                    "QUAI": "QUAI",
                                    "R": "ROUTE",
                                    "RES": "RESIDENCE",
                                    "ROC": self.default,
                                    "RPT": self.default,
                                    "RTE": "ROUTE",
                                    "RUE": "RUE",
                                    "RUE ": "RUE",
                                    "RLE": "RUELLE",
                                    "SEN": "SENTIER",
                                    "SQ": "SQUARE",
                                    "TRA": self.default,
                                    "VLA": "VILLAGE/VOIE LARGE",
                                    "VLGE": "VILLAGE/VOIE LARGE",
                                    "VGE": "VILLAGE/VOIE LARGE",
                                    "VOIE": "VOIE",
                                    "ZI": self.default
                                }
                                siren_voie = type_voie_mapping.get(siren_row["typeVoieEtablissement"].strip())
                                siren_adresse = ""
                                if siren_row["numeroVoieEtablissement"].strip():
                                    siren_adresse += siren_row["numeroVoieEtablissement"].strip() + " "
                                if siren_row["indiceRepetitionEtablissement"].strip():
                                    siren_adresse += siren_row["indiceRepetitionEtablissement"].strip() + " "
                                if siren_voie:
                                    siren_adresse += siren_voie + " "
                                siren_adresse += siren_row["libelleVoieEtablissement"]

                                siren_prenom_columns = [
                                    siren_row["prenom1UniteLegale"],
                                    siren_row["prenom2UniteLegale"],
                                    siren_row["prenom3UniteLegale"],
                                    siren_row["prenom4UniteLegale"],
                                ]
                                siren_prenom_unite = ""
                                for prenom in siren_prenom_columns:
                                    if prenom:
                                        if siren_prenom_unite != "":
                                            siren_prenom_unite += " || "
                                        siren_prenom_unite += prenom

                                siren_enseigne_list = [
                                    siren_row["enseigne1Etablissement"],
                                    siren_row["enseigne2Etablissement"],
                                    siren_row["enseigne3Etablissement"],
                                ]
                                siren_enseigne = ""
                                for enseigne_unit in siren_enseigne_list:
                                    if enseigne_unit:
                                        if siren_enseigne != "":
                                            siren_enseigne += ", "
                                        siren_enseigne += enseigne_unit

                                naf = siren_row["activitePrincipaleEtablissement"]
                                match naf:
                                    case "55.10Z":
                                        naf += " - Hôtels et hébergement similaire"
                                    case "55.20Z":
                                        naf += " - Hébergement touristique et autre hébergement de courte durée"
                                    case "55.30Z":
                                        naf += " - Terrains de camping et parcs pour caravanes ou véhicules de loisirs"
                                    case "55.90Z":
                                        naf += " - Autres hébergements"

                                siren = siren_row["siren"].strip()
                                siret = siren_row["siret"].strip()
                                dateCreationEtablissement = siren_row["dateCreationEtablissement"].strip()
                                trancheEffectifsEtablissement = siren_row["trancheEffectifsEtablissement"].strip()
                                activitePrincipaleRegistreMetiersEtablissement = siren_row[
                                    "activitePrincipaleRegistreMetiersEtablissement"].strip()
                                etablissementSiege = siren_row["etablissementSiege"].strip()
                                categorieJuridiqueUniteLegale = siren_row["categorieJuridiqueUniteLegale"].strip()
                                denominationUniteLegale = siren_row["denominationUniteLegale"].strip()
                                sexeUniteLegale = siren_row["sexeUniteLegale"].strip()
                                nomUniteLegale = siren_row["nomUniteLegale"].strip()
                                nomUsageUniteLegale = siren_row["nomUsageUniteLegale"].strip()
                                prenomUniteLegale = siren_prenom_unite.strip()
                                activitePrincipaleEtablissement = naf
                                trancheEffectifsUniteLegale = siren_row["trancheEffectifsUniteLegale"].strip()
                                complementAdresseEtablissement = siren_row[
                                    "complementAdresseEtablissement"].strip()
                                adresse = siren_adresse.strip()
                                libelleCommuneEtablissement = siren_ville.strip()
                                codePostalEtablissement = siren_row["codePostalEtablissement"].strip()
                                codeCedexEtablissement = siren_row["codeCedexEtablissement"].strip()
                                libelleCedexEtablissement = siren_row["libelleCedexEtablissement"].strip()
                                enseigne = siren_enseigne.strip()
                                denominationUsuelleEtablissement = siren_row[
                                    "denominationUsuelleEtablissement"].strip()

                with open(root_path + "/test/test_siren/merge_siren_respartner.csv", "a",
                          newline="", encoding="utf8") as merge_file:
                    writer = csv.DictWriter(merge_file, fieldnames=self.fieldsnames_merge)
                    writer.writerow({
                        self.fieldsnames_merge[1]: res_id,
                        self.fieldsnames_merge[2]: siren,
                        self.fieldsnames_merge[3]: siret,
                        self.fieldsnames_merge[4]: dateCreationEtablissement,
                        self.fieldsnames_merge[5]: trancheEffectifsEtablissement,
                        self.fieldsnames_merge[6]: activitePrincipaleRegistreMetiersEtablissement,
                        self.fieldsnames_merge[7]: etablissementSiege,
                        self.fieldsnames_merge[8]: categorieJuridiqueUniteLegale,
                        self.fieldsnames_merge[9]: denominationUniteLegale,
                        self.fieldsnames_merge[10]: sexeUniteLegale,
                        self.fieldsnames_merge[11]: nomUniteLegale,
                        self.fieldsnames_merge[12]: nomUsageUniteLegale,
                        self.fieldsnames_merge[13]: prenomUniteLegale,
                        self.fieldsnames_merge[14]: activitePrincipaleEtablissement,
                        self.fieldsnames_merge[15]: trancheEffectifsUniteLegale,
                        self.fieldsnames_merge[16]: complementAdresseEtablissement,
                        self.fieldsnames_merge[17]: adresse,
                        self.fieldsnames_merge[18]: libelleCommuneEtablissement,
                        self.fieldsnames_merge[19]: codePostalEtablissement,
                        self.fieldsnames_merge[20]: codeCedexEtablissement,
                        self.fieldsnames_merge[21]: libelleCedexEtablissement,
                        self.fieldsnames_merge[22]: res_name,
                        self.fieldsnames_merge[23]: enseigne,
                        self.fieldsnames_merge[24]: denominationUsuelleEtablissement,
                        self.fieldsnames_merge[25]: res_emails,
                        self.fieldsnames_merge[26]: res_phone,
                        self.fieldsnames_merge[27]: activity_ids,
                        self.fieldsnames_merge[28]: country_id,
                        self.fieldsnames_merge[29]: user_id,
                        self.fieldsnames_merge[30]: is_company,
                        self.fieldsnames_merge[31]: partner_gid,
                        self.fieldsnames_merge[32]: company_registry,
                        self.fieldsnames_merge[33]: company_name,
                        self.fieldsnames_merge[34]: company_id,
                        self.fieldsnames_merge[35]: comment,
                        self.fieldsnames_merge[36]: street2,
                        self.fieldsnames_merge[37]: industry_id,
                        self.fieldsnames_merge[38]: parent_id,
                        self.fieldsnames_merge[39]: ref_company_ids,
                        self.fieldsnames_merge[40]: category_id,
                        self.fieldsnames_merge[41]: company_type,
                        self.fieldsnames_merge[42]: mobile,
                        self.fieldsnames_merge[43]: phone_mobile_search,
                    })

    def test_add_siren_to_merge_siren_respartner(self):
        count = 0
        with open(root_path + "/test/test_siren/merge_siren_respartner.csv", "r") as merge_file:
            merge_reader = csv.DictReader(merge_file)
            merge_set = set()
            for merge_record in merge_reader:
                merge_set.add(merge_record["siren"])
        with open(root_path + "/siren/siren_to_merge.csv", "r", encoding="utf8") as siren_file:
            siren_reader = csv.DictReader(siren_file)
            for siren_record in siren_reader:
                if siren_record["siren"] not in merge_set:
                    count += 1
                    print(count)
                    ville = siren_record["libelleCommuneEtablissement"]
                    if "PARIS " in ville:
                        ville = ville.split(" ")
                        ville = ville[0]
                    type_voie_mapping = {
                        "": self.default,
                        "ALL": "ALLEE",
                        "AV": "AVENUE",
                        "BD": "BOULEVARD",
                        "CAMI": "CHEMIN",
                        "CAR": "CARREFOUR",
                        "CITE": "CITE",
                        "CHE": "CHEMIN",
                        "CHEM": "CHEMIN",
                        "CHS": "CHAUSSEE",
                        "CLOS": "CLOS",
                        "COR": self.default,
                        "COUR": "COUR",
                        "COTE": "COTE",
                        "CRS": "COURS",
                        "DOM": "DOMAINE",
                        "ESP": "ESPLANADE",
                        "FG": "FAUBOURG",
                        "GR": "GRANDE RUE",
                        "HAM": "HAMEAU",
                        "IMP": "IMPASSE",
                        "LD": "LIEU-DIT",
                        "LOT": "LOTISSEMENT",
                        "MTE": self.default,
                        "PAS": "PASSAGE",
                        "PARC": "PARC",
                        "PL": "PLACE",
                        "PLT": self.default,
                        "PLN": "PLAINE",
                        "PONT": "PONT",
                        "PORT": "PORT",
                        "PRO": "PROMENADE",
                        "PRV": self.default,
                        "QUA": "QUARTIER",
                        "QUAI": "QUAI",
                        "R": "ROUTE",
                        "RES": "RESIDENCE",
                        "ROC": self.default,
                        "RPT": self.default,
                        "RTE": "ROUTE",
                        "RUE": "RUE",
                        "RUE ": "RUE",
                        "RLE": "RUELLE",
                        "SEN": "SENTIER",
                        "SQ": "SQUARE",
                        "TRA": self.default,
                        "VLA": "VILLAGE/VOIE LARGE",
                        "VLGE": "VILLAGE/VOIE LARGE",
                        "VGE": "VILLAGE/VOIE LARGE",
                        "VOIE": "VOIE",
                        "ZI": self.default
                    }
                    siren_voie = type_voie_mapping.get(siren_record["typeVoieEtablissement"].strip())
                    siren_adresse = ""
                    if siren_record["numeroVoieEtablissement"].strip():
                        siren_adresse += siren_record["numeroVoieEtablissement"].strip() + " "
                    if siren_record["indiceRepetitionEtablissement"].strip():
                        siren_adresse += siren_record["indiceRepetitionEtablissement"].strip() + " "
                    if siren_voie:
                        siren_adresse += siren_voie + " "
                    siren_adresse += siren_record["libelleVoieEtablissement"]
                    adresse = siren_adresse.strip()

                    siren_prenom_columns = [
                        siren_record["prenom1UniteLegale"],
                        siren_record["prenom2UniteLegale"],
                        siren_record["prenom3UniteLegale"],
                        siren_record["prenom4UniteLegale"],
                    ]
                    siren_prenom_unite = ""
                    for prenom in siren_prenom_columns:
                        if prenom:
                            if siren_prenom_unite != "":
                                siren_prenom_unite += " || "
                            siren_prenom_unite += prenom
                    prenomUniteLegale = siren_prenom_unite.strip()

                    siren_enseigne_list = [
                        siren_record["enseigne1Etablissement"],
                        siren_record["enseigne2Etablissement"],
                        siren_record["enseigne3Etablissement"],
                    ]
                    siren_enseigne = ""
                    for enseigne_unit in siren_enseigne_list:
                        if enseigne_unit:
                            if siren_enseigne != "":
                                siren_enseigne += ", "
                            siren_enseigne += enseigne_unit
                    enseigne = siren_enseigne.strip()

                    with open(root_path + "/test/test_siren/merge_siren_respartner.csv", "a",
                              newline="") as merge_file:
                        writer = csv.DictWriter(merge_file, fieldnames=self.fieldsnames_merge)
                        writer.writerow({
                            self.fieldsnames_merge[1]: "siren",
                            self.fieldsnames_merge[2]: siren_record["siren"],
                            self.fieldsnames_merge[3]: siren_record["siret"],
                            self.fieldsnames_merge[4]: siren_record["dateCreationEtablissement"],
                            self.fieldsnames_merge[5]: siren_record["trancheEffectifsEtablissement"],
                            self.fieldsnames_merge[6]: siren_record["activitePrincipaleRegistreMetiersEtablissement"],
                            self.fieldsnames_merge[7]: siren_record["etablissementSiege"],
                            self.fieldsnames_merge[8]: siren_record["categorieJuridiqueUniteLegale"],
                            self.fieldsnames_merge[9]: siren_record["denominationUniteLegale"],
                            self.fieldsnames_merge[10]: siren_record["sexeUniteLegale"],
                            self.fieldsnames_merge[11]: siren_record["nomUniteLegale"],
                            self.fieldsnames_merge[12]: siren_record["nomUsageUniteLegale"],
                            self.fieldsnames_merge[13]: prenomUniteLegale,
                            self.fieldsnames_merge[14]: siren_record["activitePrincipaleEtablissement"],
                            self.fieldsnames_merge[15]: siren_record["trancheEffectifsUniteLegale"],
                            self.fieldsnames_merge[16]: siren_record["complementAdresseEtablissement"],
                            self.fieldsnames_merge[17]: adresse,
                            self.fieldsnames_merge[18]: ville,
                            self.fieldsnames_merge[19]: siren_record["codePostalEtablissement"],
                            self.fieldsnames_merge[20]: siren_record["codeCedexEtablissement"],
                            self.fieldsnames_merge[21]: siren_record["libelleCedexEtablissement"],
                            self.fieldsnames_merge[22]: "",
                            self.fieldsnames_merge[23]: enseigne,
                            self.fieldsnames_merge[24]: siren_record["denominationUsuelleEtablissement"],
                            self.fieldsnames_merge[25]: "",
                            self.fieldsnames_merge[26]: "",
                            self.fieldsnames_merge[27]: "",
                            self.fieldsnames_merge[28]: "",
                            self.fieldsnames_merge[29]: "",
                            self.fieldsnames_merge[30]: "",
                            self.fieldsnames_merge[31]: "",
                            self.fieldsnames_merge[32]: "",
                            self.fieldsnames_merge[33]: "",
                            self.fieldsnames_merge[34]: "",
                            self.fieldsnames_merge[35]: "",
                            self.fieldsnames_merge[36]: "",
                            self.fieldsnames_merge[37]: "",
                            self.fieldsnames_merge[38]: "",
                            self.fieldsnames_merge[39]: "",
                            self.fieldsnames_merge[40]: "",
                            self.fieldsnames_merge[41]: "",
                            self.fieldsnames_merge[42]: "",
                            self.fieldsnames_merge[43]: "",
                        })

    def test_add_zip_to_res_record(self):
        with open(root_path + "/test/test_siren/merge_siren_respartner.csv", "w",
                  newline="") as merge_file:
            writer = csv.DictWriter(merge_file, fieldnames=self.fieldsnames_merge)
            writer.writeheader()

        with open(root_path + "/test/test_siren/merge_siren_respartner_old.csv", "r") as merge_file_old:
            merge_reader = csv.DictReader(merge_file_old)
            for merge_record in merge_reader:
                code_postal_res = merge_record["codePostalEtablissement"].strip()
                if code_postal_res == "":
                    with open(root_path + "/res_partner/res_partner.csv", "r", encoding="utf8") as res_partner_file:
                        res_partner_reader = csv.DictReader(res_partner_file)
                        for res_partner_record in res_partner_reader:
                            id_res_partner = res_partner_record["id"].replace("__export__.res_partner_", "").split("_")
                            id_res_partner = id_res_partner[0].strip()
                            if merge_record["id_respartner"].strip() == id_res_partner:
                                code_postal_res = res_partner_record["zip"].strip()
                with open(root_path + "/test/test_siren/merge_siren_respartner.csv", "a", newline="") as merge_file:
                    merge_writer = csv.DictWriter(merge_file, fieldnames=self.fieldsnames_merge)
                    merge_writer.writerow({
                        self.fieldsnames_merge[1]: merge_record[self.fieldsnames_merge[1]],
                        self.fieldsnames_merge[2]: merge_record[self.fieldsnames_merge[2]],
                        self.fieldsnames_merge[3]: merge_record[self.fieldsnames_merge[3]],
                        self.fieldsnames_merge[4]: merge_record[self.fieldsnames_merge[4]],
                        self.fieldsnames_merge[5]: merge_record[self.fieldsnames_merge[5]],
                        self.fieldsnames_merge[6]: merge_record[self.fieldsnames_merge[6]],
                        self.fieldsnames_merge[7]: merge_record[self.fieldsnames_merge[7]],
                        self.fieldsnames_merge[8]: merge_record[self.fieldsnames_merge[8]],
                        self.fieldsnames_merge[9]: merge_record[self.fieldsnames_merge[9]],
                        self.fieldsnames_merge[10]: merge_record[self.fieldsnames_merge[10]],
                        self.fieldsnames_merge[11]: merge_record[self.fieldsnames_merge[11]],
                        self.fieldsnames_merge[12]: merge_record[self.fieldsnames_merge[12]],
                        self.fieldsnames_merge[13]: merge_record[self.fieldsnames_merge[13]],
                        self.fieldsnames_merge[14]: merge_record[self.fieldsnames_merge[14]],
                        self.fieldsnames_merge[15]: merge_record[self.fieldsnames_merge[15]],
                        self.fieldsnames_merge[16]: merge_record[self.fieldsnames_merge[16]],
                        self.fieldsnames_merge[17]: merge_record[self.fieldsnames_merge[17]],
                        self.fieldsnames_merge[18]: merge_record[self.fieldsnames_merge[18]],
                        self.fieldsnames_merge[19]: code_postal_res,
                        self.fieldsnames_merge[20]: merge_record[self.fieldsnames_merge[20]],
                        self.fieldsnames_merge[21]: merge_record[self.fieldsnames_merge[21]],
                        self.fieldsnames_merge[22]: merge_record[self.fieldsnames_merge[22]],
                        self.fieldsnames_merge[23]: merge_record[self.fieldsnames_merge[23]],
                        self.fieldsnames_merge[24]: merge_record[self.fieldsnames_merge[24]],
                        self.fieldsnames_merge[25]: merge_record[self.fieldsnames_merge[25]],
                        self.fieldsnames_merge[26]: merge_record[self.fieldsnames_merge[26]],
                        self.fieldsnames_merge[27]: merge_record[self.fieldsnames_merge[27]],
                        self.fieldsnames_merge[28]: merge_record[self.fieldsnames_merge[28]],
                        self.fieldsnames_merge[29]: merge_record[self.fieldsnames_merge[29]],
                        self.fieldsnames_merge[30]: merge_record[self.fieldsnames_merge[30]],
                        self.fieldsnames_merge[31]: merge_record[self.fieldsnames_merge[31]],
                        self.fieldsnames_merge[32]: merge_record[self.fieldsnames_merge[32]],
                        self.fieldsnames_merge[33]: merge_record[self.fieldsnames_merge[33]],
                        self.fieldsnames_merge[34]: merge_record[self.fieldsnames_merge[34]],
                        self.fieldsnames_merge[35]: merge_record[self.fieldsnames_merge[35]],
                        self.fieldsnames_merge[36]: merge_record[self.fieldsnames_merge[36]],
                        self.fieldsnames_merge[37]: merge_record[self.fieldsnames_merge[37]],
                        self.fieldsnames_merge[38]: merge_record[self.fieldsnames_merge[38]],
                        self.fieldsnames_merge[39]: merge_record[self.fieldsnames_merge[39]],
                        self.fieldsnames_merge[40]: merge_record[self.fieldsnames_merge[40]],
                        self.fieldsnames_merge[41]: merge_record[self.fieldsnames_merge[41]],
                        self.fieldsnames_merge[42]: merge_record[self.fieldsnames_merge[42]],
                        self.fieldsnames_merge[43]: merge_record[self.fieldsnames_merge[43]],
                    })

    def test_list_NAF_code(self):
        with open(root_path + "/siren/siren_to_merge.csv", "r", encoding="utf8") as siren_file:
            siren_reader = csv.DictReader(siren_file)
            naf = set()
            for row in list(siren_reader):
                naf.add(row["activitePrincipaleEtablissement"])
            for code in naf:
                print(code)
