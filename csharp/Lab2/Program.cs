using System;

public class Polynomial
{
    public double[] coeffs;

    public Polynomial(params double[] coefficients)
    {
        coeffs = coefficients;
    }

    public double Calculate(double x)
    {
        double result = 0;
        for (int power = 0; power < coeffs.Length; power++)
        {
            result += coeffs[power] * Math.Pow(x, power);
        }
        return result;
    }

    public Polynomial Add(Polynomial other)
    {
        int maxLength = Math.Max(coeffs.Length, other.coeffs.Length);
        double[] result = new double[maxLength];

        for (int i = 0; i < maxLength; i++)
        {
            double a = (i < coeffs.Length) ? coeffs[i] : 0;
            double b = (i < other.coeffs.Length) ? other.coeffs[i] : 0;
            result[i] = a + b;
        }
        
        return new Polynomial(result);
    }

    public Polynomial Multiply(Polynomial other)
    {
        double[] result = new double[coeffs.Length + other.coeffs.Length - 1];
        
        for (int i = 0; i < coeffs.Length; i++)
        {
            for (int j = 0; j < other.coeffs.Length; j++)
            {
                result[i + j] += coeffs[i] * other.coeffs[j];
            }
        }
        
        return new Polynomial(result);
    }

    public override string ToString()
    {
        string result = "";
        for (int i = 0; i < coeffs.Length; i++)
        {
            if (i == 0)
                result += $"{coeffs[i]}";
            else
                result += $" + {coeffs[i]}x^{i}";
        }
        return result == "" ? "0" : result;
    }
}

class Program
{
    static void Main()
    {
        Polynomial p1 = new Polynomial(1, 2);    // 1 + 2x
        Polynomial p2 = new Polynomial(3, 4, 5); // 3 + 4x + 5x^2

        Console.WriteLine("Многочлен 1: " + p1);
        Console.WriteLine("Многочлен 2: " + p2);
        
        Console.WriteLine("\nСложение:");
        Polynomial sum = p1.Add(p2);
        Console.WriteLine(sum);
        
        Console.WriteLine("\nУмножение:");
        Polynomial product = p1.Multiply(p2);
        Console.WriteLine(product);
        
        Console.WriteLine("\nВычисление p1 в точке x=2:");
        Console.WriteLine(p1.Calculate(2));
    }
}