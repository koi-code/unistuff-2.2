Console.Write("Введите символ: ");
        
string? input = Console.ReadLine();

char symbol = !string.IsNullOrEmpty(input) ? input[0] : 'a';

Console.Write("Введите высоту пирамиды: ");
int height = int.Parse(Console.ReadLine() ?? "1");

for (int row = 1; row <= height; row++)
{
    
    for (int space = 0; space < height - row; space++)
    {
        Console.Write(' ');
    }
    
    for (int x = 0; x < 2 * row - 1; x++)
    {
        Console.Write(symbol);
    }
    Console.WriteLine();
}