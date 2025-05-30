using System;

abstract class Shape
{
    public abstract double SurfaceArea();
}

class Parallelepiped : Shape
{
    private double a;
    private double b;
    private double c;
    
    public Parallelepiped(double a, double b, double c)
    {
        this.a = a;
        this.b = b;
        this.c = c;
    }
    
    public override double SurfaceArea()
    {
        return 2 * (a * b + a * c + b * c);
    }
}

class Tetrahedron : Shape
{
    private double edge;
    
    public Tetrahedron(double edge)
    {
        this.edge = edge;
    }
    
    public override double SurfaceArea()
    {
        return Math.Sqrt(3) * edge * edge;
    }
}

class Sphere : Shape
{
    private double radius;
    
    public Sphere(double radius)
    {
        this.radius = radius;
    }
    
    public override double SurfaceArea()
    {
        return 4 * Math.PI * radius * radius;
    }
}

class Program
{
    static void Main()
    {

        Shape[] shapes = new Shape[]
        {
            new Parallelepiped(2, 3, 4),
            new Tetrahedron(5),
            new Sphere(3)
        };
        

        foreach (Shape shape in shapes)
        {
            Console.WriteLine($"Площадь поверхности: {shape.SurfaceArea():F2}");
        }
    }
}