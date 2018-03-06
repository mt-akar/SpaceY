using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Shapes;

namespace Space_Y
{
    public partial class Solution : Window
    {
        Square[,] a = new Square[5,5];

        public Solution(ref string[,] sol)
        {
            InitializeComponent();
            
            StreamReader layoutReader = new StreamReader(@"C:\SpaceY\NYTC\layout.txt");
            StreamReader solutionReader = new StreamReader(@"C:\SpaceY\NYTC\solution.txt");
            for (int i = 0; i < 5; i++)
            {
                for (int j = 0; j < 5; j++)
                {
                    char readLay = (char)layoutReader.Read();
                    string writeLay = readLay == '0' ? "" : readLay.ToString();

                    if (writeLay == "e")
                    {
                        a[i, j] = new Square(i, j, "", Color.FromArgb(255, 0, 0, 0));
                    }
                    else
                    {
                        a[i, j] = new Square(i, j, writeLay, Color.FromArgb(255, 255, 255, 255));
                    }
                    a[i, j].Text = ((char)solutionReader.Read()).ToString();
                }
            }

            #region Data Context Bindings

            sq00.DataContext = a[0, 0];
            sq01.DataContext = a[0, 1];
            sq02.DataContext = a[0, 2];
            sq03.DataContext = a[0, 3];
            sq04.DataContext = a[0, 4];
            sq10.DataContext = a[1, 0];
            sq11.DataContext = a[1, 1];
            sq12.DataContext = a[1, 2];
            sq13.DataContext = a[1, 3];
            sq14.DataContext = a[1, 4];
            sq20.DataContext = a[2, 0];
            sq21.DataContext = a[2, 1];
            sq22.DataContext = a[2, 2];
            sq23.DataContext = a[2, 3];
            sq24.DataContext = a[2, 4];
            sq30.DataContext = a[3, 0];
            sq31.DataContext = a[3, 1];
            sq32.DataContext = a[3, 2];
            sq33.DataContext = a[3, 3];
            sq34.DataContext = a[3, 4];
            sq40.DataContext = a[4, 0];
            sq41.DataContext = a[4, 1];
            sq42.DataContext = a[4, 2];
            sq43.DataContext = a[4, 3];
            sq44.DataContext = a[4, 4];

            #endregion

            Icon = BitmapFrame.Create(new Uri("pack://application:,,,/spacey-icon.ico", UriKind.RelativeOrAbsolute));
        }
    }
}
