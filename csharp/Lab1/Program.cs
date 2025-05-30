/*

Вариант 8.

При помощи циклов for изобразите на экране пирамиду из
символов, образец которых введён с клавиатуры. Например, введён символ
‘x’. Пирамида должна выглядеть следующим образом:
Вся пирамида должна быть высотой не 5 линий, как изображено здесь,
а линий ( ввести с клавиатуры). Одним из способов её построения может
служить использование двух вложенных циклов, из которых внутренний
будет заниматься печатаньем символов ‘x’ и пробелов, а другой
осуществлять переход на одну строку вниз. Расположить пирамиду по центру
экрана.

*/

/*

Отчет: https://docs.google.com/document/d/19cQs-aKAwjuZ5MeU0GOzp1yZErqC-wm1BoVlWcEjl9A/edit?usp=sharing

*/

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