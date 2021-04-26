#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
#include <random>
#include <time.h>

using namespace std;




ifstream fin("input.txt");
ofstream dout("distanta.txt");
ofstream tout("timp.txt");

random_device rd1;
mt19937 e1(rd1());

random_device rd2;
mt19937 e2(rd2());
uniform_real_distribution<> dist_real(0, 1);

int nrOrase;
int dimPop = 100;
float Best = 3.40282e+038;
float crossProb = 0.5;
float mutProb = 0.01;
int nrIt = 1000;

struct Oras {
    int nr_Oras;
    float x;
    float y;
};

class Ruta {
public:
    vector<int> ruta;
    float fitness = 0;
    float lungime = 0;
    Ruta(vector <int> ruta2) {
        ruta = ruta2;
    }
};

bool operator>(const Ruta& ruta1, const Ruta& ruta2)
{
    return ruta1.fitness > ruta2.fitness;
}

vector<int> randvect(int nrOrase) {
    vector<int> ruta;
    while (ruta.size() < nrOrase)
    {
        ruta.push_back(ruta.size() + 1);
    }
    for (int ii = nrOrase - 1; ii >= 0; --ii)
    {
        int jj = rand() % (ii + 1);
        swap(ruta[ii], ruta[jj]);
    }
    return ruta;
}

float eval(vector<int>& traseu, vector<vector<float>>& distanta) {
    float lungime = 0;
    for (int ii = 0; ii < nrOrase - 1; ii++)
    {
        int x = traseu[ii];
        int y = traseu[ii + 1];
        lungime = lungime + distanta[x - 1][y - 1];
    }
    int x = traseu[nrOrase - 1];
    int y = traseu[0];
    lungime = lungime + distanta[x - 1][y - 1];
    return lungime;
}
void Simulated_Annealing(vector<Oras>& harta, vector<vector<float>>& distanta)
{
    clock_t time = clock();
    uniform_int_distribution<> dist_int(0, nrOrase - 1);

    int t = 0;
    float T = 100;
    vector<int> vc;
    vc = randvect(nrOrase);
    //eval1(vc);
    do {
        t = 0;
        do {
            vector<int> poz;
            vector<int> vn = vc;
            poz.push_back(dist_int(e1));
            poz.push_back(dist_int(e1));
            sort(poz.begin(), poz.end());
            reverse(vn.begin() + poz[0], vn.begin() + poz[1]);
            poz.push_back(dist_int(e1));
            sort(poz.begin(), poz.end());
            rotate(vn.begin() + poz[0], vn.begin() + poz[1], vn.begin() + poz[2]);
            /*
            while (position1 < position2)
            {
                swap(vn[position1], vn[position2]);
                position1++;
                position2--;
            }
            */
            //swap(vn[dist_int(e1)], vn[dist_int(e1)]);
            if (eval(vn, distanta) < eval(vc, distanta))
                vc = vn;
            else if (dist_real(e2) < exp(-abs(eval(vn, distanta) - eval(vc, distanta)) / T))
                vc = vn;
            t++;
        } while (t < 1000);
        //cout << eval(vc, distanta) << "\n";
        T *= 0.9;
        //cout << T << "*\n";
    } while (T >= 0.00000001);
    cout << "\n";
    time = clock() - time;
    cout << ((float)time) / CLOCKS_PER_SEC << " " << eval(vc, distanta) << "\n";
    tout << ((float)time) / CLOCKS_PER_SEC << "\n";
    dout << eval(vc, distanta) << "\n";
    //eval1(vc);
}

void Generare_populatie_initiala(vector <Ruta>& sol)
{
    while (sol.size() < dimPop)
    {
        sol.push_back(Ruta(randvect(nrOrase)));
    }
}
void ProbAfisare(int& generatie, vector <Ruta>& sol, int dimPop, vector<float> &ProbInd, vector<float> &ProbAcc )
{

    float medie = 0, fitnessTotal = 0;
    for (int ii = 0; ii < dimPop; ii++)
    {
        fitnessTotal = fitnessTotal + sol[ii].fitness;
    }
    //medie = medie / dimPop;

    for (int ii = 0; ii < dimPop; ii++)
        ProbInd.push_back(sol[ii].fitness / fitnessTotal);
    ProbAcc.push_back(0);
    for (int ii = 0; ii < dimPop; ii++)
        ProbAcc.push_back(ProbAcc[ii] + ProbInd[ii]);
    ProbAcc[dimPop] = 1;

    /*
    for (int ii = 0; ii < 5; ii++)
    {
        cout << sol[ii].valoare << " ";
        for (int jj = 0; jj < n * dim; jj++)
            cout << float(sol[ii].cromozon[jj]);
        cout << " " << sol[ii].fitness << " " << ProbInd[ii] << " " << ProbAcc[ii] << "\n";
    }
    */
    cout << generatie << " " << sol[0].lungime << "\n";
    //cout << "**************\n";
    if (sol[0].lungime < Best)
    {
        Best = sol[0].lungime;
    }
}
void AfisarePopulatie(vector <Ruta>& sol)
{
    for (int ii = 0; ii < sol.size(); ii++)
    {
        for (int jj = 0; jj < nrOrase; jj++)
        {
            cout << sol[ii].ruta[jj] << " ";
        }
        cout << sol[ii].lungime << "\n\n";
    }
}

void Incrucisare(int dimPop, vector<Ruta>& matingPool, vector<Ruta>& newSol)
{
    uniform_int_distribution<> dist_int(0, dimPop - 1);
    uniform_int_distribution<> dist_int1(0, nrOrase - 1);
    for (int i = 0; i < dimPop / 2; i++)
    {
        vector<int>parinte1 = matingPool[dist_int(e1)].ruta;
        vector<int>parinte2 = matingPool[dist_int(e1)].ruta;
        if (dist_real(e2)<0.5)
        {
            int poz = dist_int1(e1);
            vector<int> restGena1 = parinte1;
            vector<int> restGena2 = parinte2;
            for (int k = 0; k < 2; k++)
            {
                vector<int> Copil1, Copil2;
                for (int i = 0; i < poz; i++)
                {
                    Copil1.push_back(parinte1[i]);
                    Copil2.push_back(parinte2[i]);
                    for (int j = 0; j < restGena2.size(); j++)
                    {
                        if (restGena2[j] == Copil1[i]) {
                            restGena2.erase(restGena2.begin() + j);
                            break;
                        }
                    }
                    for (int j = 0; j < restGena1.size(); j++)
                    {
                        if (restGena1[j] == Copil2[i]) {
                            restGena1.erase(restGena1.begin() + j);
                            break;
                        }
                    }
                }
                Copil1.insert(Copil1.end(), restGena2.begin(), restGena2.end());
                Copil2.insert(Copil2.end(), restGena1.begin(), restGena1.end());
                parinte1 = Copil1;
                parinte2 = Copil2;
            }
        }
        newSol.push_back(Ruta(parinte1));
        newSol.push_back(Ruta(parinte2));
    }
    
}
void CalculFitness(vector <Ruta>& sol, vector<vector<float>> &distanta) {
    //cout << "-------------Fitness----------------\n";
    for (int ii = 0; ii < sol.size(); ii++)
    {
        sol[ii].lungime = 0;
        for (int jj = 0; jj < nrOrase - 1; jj++)
        {
            int x = sol[ii].ruta[jj];
            int y = sol[ii].ruta[jj + 1];
            //cout << "(" << x << ", " << y << ")" << " ";
            //cout << "(" << distanta[x-1][y-1] << ")" << " ";
            sol[ii].lungime = sol[ii].lungime + distanta[x - 1][y - 1];
        }
        int x = sol[ii].ruta[nrOrase - 1];
        int y = sol[ii].ruta[0];
        //cout << "(" << x << ", " << y << ")" << " ";
        //cout << "(" << distanta[x - 1][y - 1] << ")" << " ";
        sol[ii].lungime = sol[ii].lungime + distanta[x - 1][y - 1];
        sol[ii].fitness = 1 / sol[ii].lungime;
        //cout << sol[ii].lungime << " " << sol[ii].fitness << "\n";
    }
}
void AlgoritmGeneticXSimulatedAnnealing(vector<Oras>& harta, vector<vector<float>>& distanta)
{
    Best = 3.40282e+038;
    clock_t time = clock();
    int generatie = 0;
    crossProb = 0.3;
    mutProb = 0.01;

    vector <Ruta> sol;
    uniform_int_distribution<> dist_int(0, nrOrase - 1);
    vector<float> ProbInd, ProbAcc;

    Generare_populatie_initiala(sol);
    //cout << "-------------Pop init----------------\n";
    //AfisarePopulatie(sol);
    CalculFitness(sol, distanta);
    ProbAfisare(generatie, sol, dimPop, ProbInd, ProbAcc);
    while (generatie < nrIt)
    {
        generatie++;
        vector <Ruta> newSol, matingPool;
        //selectie tip ruleta
        while (matingPool.size() < dimPop)
        {
            float r = dist_real(e2);
            for (int ii = 0; ii < dimPop; ii++)
                if (ProbAcc[ii] <= r && r <= ProbAcc[ii + 1])
                {
                    //cout << "**" << r << " " << ii << "\n";
                    matingPool.push_back(sol[ii]);
                    break;
                }
        }
        for (int i = 0; i < dimPop; i++)
            for (int j = 0; j < nrOrase; j++)
            {
                float p = dist_real(e2);
                if (p < mutProb)
                {
                    vector<int> poz;
                    vector<int> vn = matingPool[i].ruta;
                    poz.push_back(dist_int(e1));
                    poz.push_back(dist_int(e1));
                    sort(poz.begin(), poz.end());
                    reverse(vn.begin() + poz[0], vn.begin() + poz[1]);
                    poz.push_back(dist_int(e1));
                    sort(poz.begin(), poz.end());
                    rotate(vn.begin() + poz[0], vn.begin() + poz[1], vn.begin() + poz[2]);

                    matingPool[i].ruta = vn;
                }
            }
        Incrucisare(dimPop, matingPool, newSol);
        //cout << "-------------Copii----------------\n";
        //AfisarePopulatie(newSol);
        sol.erase(sol.begin() + dimPop - 98, sol.end());
        sol.insert(sol.end(), newSol.begin(), newSol.end());
        //cout << "-------------Pop. marita----------------\n";
        //AfisarePopulatie(sol);
        CalculFitness(sol, distanta);

        sort(sol.begin(), sol.end(), greater<Ruta>());
        //cout << "-------------Pop. sortata----------------\n";
        //AfisarePopulatie(sol);

        sol.erase(sol.begin() + dimPop - 4, sol.end());
        //newSol.erase(newSol.begin(), newSol.end());
        //cout << "-------------Pop. nou----------------\n";
        //AfisarePopulatie(sol);
        while (sol.size() < dimPop)
        {
            sol.push_back(Ruta(randvect(nrOrase)));
        }
        ProbAfisare(generatie, sol, dimPop, ProbInd, ProbAcc);
    }

    int t = 0;
    float T = 100;
    vector<int> vc;
    vc = sol[0].ruta;
    do {
        t = 0;
        do {
            vector<int> poz;
            vector<int> vn = vc;
            poz.push_back(dist_int(e1));
            poz.push_back(dist_int(e1));
            sort(poz.begin(), poz.end());
            reverse(vn.begin() + poz[0], vn.begin() + poz[1]);
            poz.push_back(dist_int(e1));
            sort(poz.begin(), poz.end());
            rotate(vn.begin() + poz[0], vn.begin() + poz[1], vn.begin() + poz[2]);
            if (eval(vn, distanta) < eval(vc, distanta))
                vc = vn;
            else if (dist_real(e2) < exp(-abs(eval(vn, distanta) - eval(vc, distanta)) / T))
                vc = vn;
            t++;
        } while (t < 1000);
        //cout << eval(vc, distanta) << "\n";
        T *= 0.9;
        //cout << T << "*\n";
    } while (T >= 0.00000001);
    Best = min(Best, eval(vc, distanta));

    time = clock() - time;
    cout << Best << " " << ((float)time) / CLOCKS_PER_SEC << "\n";
    tout << ((float)time) / CLOCKS_PER_SEC << "\n";
    dout << Best << "\n";
}
void AlgoritmGenetic(vector<Oras> &harta, vector<vector<float>> &distanta)
{
    Best = 3.40282e+038;
    clock_t time = clock();
    int generatie = 0;
    crossProb = 0.5;
    mutProb = 0.01;
    vector <Ruta> sol;
    uniform_int_distribution<> dist_int(0, nrOrase - 1);
    vector<float> ProbInd, ProbAcc;

    Generare_populatie_initiala(sol);
    //cout << "-------------Pop init----------------\n";
    //AfisarePopulatie(sol);
    CalculFitness(sol, distanta);
    ProbAfisare(generatie, sol, dimPop, ProbInd, ProbAcc);
    while (generatie < nrIt)
    {
        generatie++;
        vector <Ruta> newSol, matingPool;
        //selectie tip ruleta
        while (matingPool.size() < dimPop)
        {
            float r = dist_real(e2);
            for (int ii = 0; ii < dimPop; ii++)
                if (ProbAcc[ii] <= r && r <= ProbAcc[ii + 1])
                {
                    //cout << "**" << r << " " << ii << "\n";
                    matingPool.push_back(sol[ii]);
                    break;
                }
        }
        for (int i = 0; i < dimPop; i++)
            for (int j = 0; j < nrOrase; j++)
            {
                float p = dist_real(e2);
                if (p < mutProb)
                {
                    int poz1, poz2;
                    poz1 = dist_int(e1);
                    do {
                        poz2 = dist_int(e1);
                    } while (poz1 == poz2);
                    swap(matingPool[i].ruta[poz1], matingPool[i].ruta[poz2]);
                }
            }
        Incrucisare(dimPop, matingPool, newSol);
        //cout << "-------------Copii----------------\n";
        //AfisarePopulatie(newSol);
        sol.insert(sol.end(), newSol.begin(), newSol.end());
        //cout << "-------------Pop. marita----------------\n";
        //AfisarePopulatie(sol);
        CalculFitness(sol, distanta);

        sort(sol.begin(), sol.end(), greater<Ruta>());
        //cout << "-------------Pop. sortata----------------\n";
        //AfisarePopulatie(sol);

        sol.erase(sol.begin() + dimPop - 5, sol.end());
        //newSol.erase(newSol.begin(), newSol.end());
        //cout << "-------------Pop. nou----------------\n";
        //AfisarePopulatie(sol);
        while (sol.size() < dimPop)
        {
            sol.push_back(Ruta(randvect(nrOrase)));
        }
        ProbAfisare(generatie, sol, dimPop, ProbInd, ProbAcc);
    }
    time = clock() - time;
    cout << Best << " " << ((float)time) / CLOCKS_PER_SEC << "\n";
    tout << ((float)time) / CLOCKS_PER_SEC << "\n";
    dout << Best << "\n";
}
int main()
{
    fin >> nrOrase;
    Oras oras;
    vector<Oras> harta;
    vector<vector<float>> distanta(nrOrase, vector<float>(nrOrase));
    while (harta.size() < nrOrase)
    {
        fin >> oras.nr_Oras >> oras.x >> oras.y;
        harta.push_back(oras);
        //cout << harta[oras.nr_Oras - 1].nr_Oras << " " << harta[oras.nr_Oras - 1].x << " " << harta[oras.nr_Oras - 1].y << "\n";
    }
    //cout << "------------Distante-----------------\n";
    for (int ii = 0; ii < nrOrase; ii++)
    {
        for (int jj = 0; jj < nrOrase; jj++)
        {
            float delta_x = abs(harta[ii].x - harta[jj].x);
            float delta_y = abs(harta[ii].y - harta[jj].y);
            distanta[ii][jj] = sqrt(delta_x * delta_x + delta_y * delta_y);
            //cout << distanta[ii][jj] << " ";
        }
        //cout << "\n";
    }
    for(int i=0;i<1; i++)
        AlgoritmGenetic(harta, distanta);
    for(int i=0;i<1; i++)
        AlgoritmGeneticXSimulatedAnnealing(harta, distanta);
    for (int i = 0; i < 1; i++)
        Simulated_Annealing(harta, distanta);
    return 0;
}
