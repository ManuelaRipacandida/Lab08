from database.impianto_DAO import ImpiantoDAO
from model.consumo_DTO import Consumo

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1


    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()


    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # TODO

        consumi_medi=[]
        for impianto in self._impianti:
            totale = 0
            contatore = 0
            lista_consumi=impianto.get_consumi()
            for consumo in lista_consumi:
                if consumo.data.month==mese:
                    totale+=consumo.kwh
                    contatore+=1
            media=totale/contatore
            consumi_medi.append((impianto.nome,media))
        return consumi_medi




    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO
        #condizione di terminazione
        if len(sequenza_parziale) == 7:
            # Controllo se è il primo costo calcolato o se questo è migliore di quello ottimo
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo=costo_corrente    # Aggiorno il costo ottimo
                self.__sequenza_ottima=sequenza_parziale.copy() # Salvo la sequenza ottima trovata

            return
        else:
            for impianto in self._impianti:
                # Calcolo del costo di spostamento: se cambio impianto rispetto al giorno precedente aggiungo 5
                if ultimo_impianto!=impianto.id:
                    costo_fisso=+5
                else:
                    costo_fisso = 0
                # Costo del giorno corrente in base al consumo dell'impianto
                costo_giono = consumi_settimana[impianto.id][giorno-1]
                sequenza_parziale.append(impianto.id)
                nuovo_costo=costo_corrente + costo_fisso + costo_giono
                # Chiamata ricorsiva per il giorno successivo
                self.__ricorsione(sequenza_parziale,giorno + 1,impianto.id,nuovo_costo,consumi_settimana)
                sequenza_parziale.pop()




    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        # TODO

        consumi_primi_giorni = {}
        for impianto in self._impianti:
            primi7 = []


            lista_consumi = impianto.get_consumi()
            for consumo in lista_consumi:
                if consumo.data.month== mese and consumo.data.day <=7:
                        c= consumo.kwh
                        primi7.append(c)

            consumi_primi_giorni[impianto.id] = primi7


        return consumi_primi_giorni


