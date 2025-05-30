using System;
using System.Collections.Generic;

abstract class Place {
    protected string Name;
    protected static List<Place> AllPlaces = new List<Place>();

    public Place(string name) {
        Name = name;
    }

    public abstract void Show();

    public void Add() {
        AllPlaces.Add(this);
    }

    public static void ShowAll() {
        foreach (Place place in AllPlaces) {
            place.Show();
        }
    }
}

class Region : Place {
    protected double Area;

    public Region(string name, double area) : base(name) {
        Area = area;
    }

    public override void Show() {
        Console.WriteLine($"Область: {Name}, Площадь: {Area} км²");
    }
}

class City : Place {
    protected int Population;

    public City(string name, int population) : base(name) {
        Population = population;
    }

    public override void Show() {
        Console.WriteLine($"Город: {Name}, Население: {Population} чел.");
    }
}

class Metropolis : City {
    protected int Skyscrapers;

    public Metropolis(string name, int population, int skyscrapers) 
        : base(name, population) {
        Skyscrapers = skyscrapers;
    }

    public override void Show() {
        Console.WriteLine($"Мегаполис: {Name}, " +
            $"Население: {Population} чел., " +
            $"Небоскрёбы: {Skyscrapers} шт.");
    }
}

class Program {
    static void Main() {
        Region region = new Region("Московская область", 44300);
        City city = new City("Казань", 1257000);
        Metropolis metro = new Metropolis("Москва", 12655000, 250);

        region.Add();
        city.Add();
        metro.Add();

        Place.ShowAll();
    }
}