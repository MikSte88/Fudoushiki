/*********************************************
 * OPL 22.1.1.0 Model
 * Author: puren
 * Creation Date: 25 kwi 2023 at 10:32:10
 *********************************************/
int N = 7; // Rozmiar planszy
int R = 18; // Liczba nierówności
int L = 4; // Liczba liczb startowych

int Nierownosci[1..R][1..2][1..2] =[[[4, 2], [5, 3]], [[4, 6], [3, 6]], [[5, 5], [4, 4]], [[3, 7], [2, 6]], [[4, 3], [3, 3]], [[2, 1], [3, 1]], [[2, 1], [2, 2]], [[2, 7], [1, 7]], [[7, 3], [7, 4]], [[3, 4], [2, 3]], [[4, 7], [5, 6]], [[7, 4], [7, 5]], [[6, 4], [5, 5]], [[6, 6], [5, 7]], [[2, 2], [3, 1]], [[4, 3], [3, 4]], [[3, 5], [2, 6]], [[4, 2], [4, 1]]];
int Liczby[1..L][1..2][1..2] =[[[5, 6], [2, 2]], [[4, 1], [3, 3]], [[6, 6], [5, 5]], [[7, 3], [2, 2]]];

dvar int X[1..N][1..N]; // Plansza
dvar boolean ZERA[1..N][1..N];
dexpr int ilosc_zer  =  sum(i in 1..N) sum(j in 1..N) ZERA[i][j];


minimize ilosc_zer; // Minimalizujemy zera
subject to {
  
forall(i in 1..N) 
	forall(j in 1..N) 
		X[i][j] >= 0; // Większe niż 0
	
forall(i in 1..N) 
	forall(j in 1..N) 
		X[i][j] <= N; //Mniejsze niż N

forall(i in 1..R) 
	(X[Nierownosci[i][1][1]][Nierownosci[i][1][2]] != 0) => // Jeżeli to nie jest zerem
	
	(X[Nierownosci[i][1][1]][Nierownosci[i][1][2]] 
	>= X[Nierownosci[i][2][1]][Nierownosci[i][2][2]]); //Uwzglednienie nierownosci

forall(i in 1..L) X[Liczby[i][1][1]][Liczby[i][1][2]] == Liczby[i][2][1]; //Uwzglednienie podanych na start liczb
forall(l in 1..N) 
	forall(i in 1..N) 
		sum(j in 1..N) 
			(X[i][j] == l) <= 1; // Jedna cyfra na rząd
forall(l in 1..N) 
	forall(i in 1..N) 
		sum(j in 1..N) 
			(X[j][i] == l) <= 1; // Jedna cyfra na kolumnę

forall(i in 1..N) 
	forall(j in 1..N) 
		(X[i][j] == 0) => (ZERA[i][j] == 1); // Większe niż 0
			
}

