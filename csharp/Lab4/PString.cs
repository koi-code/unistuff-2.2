public class Pstring : MyString
{
    public Pstring() : base() { }
    public Pstring(string s) : base(s) { }

    public Pstring Left(MyString s1, int n)
    {
        int lenS1 = 0;

        while (lenS1 < SZ && s1.str[lenS1] != '\0')
        {
            lenS1++;
        }
        
        int copyCount = Math.Min(n, lenS1);
        copyCount = Math.Min(copyCount, SZ - 1);

        
        for (int i = 0; i < copyCount; i++)
        {
            str[i] = s1.str[i];
        }
        str[copyCount] = '\0';
        return this;
    }

    public Pstring Mid(MyString s1, int s, int n)
    {
        int lenS1 = 0;
        while (lenS1 < SZ && s1.str[lenS1] != '\0')
        {
            lenS1++;
        }

        if (s >= lenS1)
        {
            str[0] = '\0';
            return this;
        }
        
        int available = lenS1 - s;
        int copyCount = Math.Min(n, available);
        copyCount = Math.Min(copyCount, SZ - 1);

        
        for (int i = 0; i < copyCount; i++)
        {
            str[i] = s1.str[s + i];
        }
        str[copyCount] = '\0';
        return this;
    }

    public Pstring Right(MyString s1, int n)
    {
        int lenS1 = 0;
        while (lenS1 < SZ && s1.str[lenS1] != '\0')
        {
            lenS1++;
        }
        
        int copyCount = Math.Min(n, lenS1);
        copyCount = Math.Min(copyCount, SZ - 1);
        int startIndex = lenS1 - copyCount;

        
        for (int i = 0; i < copyCount; i++)
        {
            str[i] = s1.str[startIndex + i];
        }
        str[copyCount] = '\0';
        return this;
    }
}