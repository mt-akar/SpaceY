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
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Space_Y
{
    public partial class MainWindow : Window
    {
        static Square[,] a = new Square[5, 5];
        static string[,] sol = new string[5, 5];
        int exceptionNumber = 0;

        public MainWindow()
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
                    sol[i, j] = ((char)solutionReader.Read()).ToString();
                }
            }
            layoutReader.Close();
            solutionReader.Close();

            StreamReader sr0 = new StreamReader(@"C:\SpaceY\NYTC\clues.txt");
            TextBoxContent acrossText = new TextBoxContent(sr0.ReadLine() + "\n" + sr0.ReadLine() + "\n" + sr0.ReadLine() + "\n" + sr0.ReadLine() + "\n" + sr0.ReadLine());
            TextBoxContent downText = new TextBoxContent(sr0.ReadToEnd());
            sr0.Close();

            StreamReader sr1 = new StreamReader(@"C:\SpaceY\NYTC\title.txt");
            TextBoxContent titleText = new TextBoxContent(sr1.ReadLine());
            sr1.Close();

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

            across.DataContext = acrossText;
            down.DataContext = downText;
            title.DataContext = titleText;
            #endregion

            double screenWidth = SystemParameters.PrimaryScreenWidth;
            double screenHeight = SystemParameters.PrimaryScreenHeight;
            Left = (screenWidth / 2) - (Width / 2);
            Top = (screenHeight / 2) - (Height / 2);

            Icon = BitmapFrame.Create(new Uri("pack://application:,,,/spacey-icon.ico", UriKind.RelativeOrAbsolute));
        }

        private void Update(object sender, RoutedEventArgs e)
        {
            StreamReader sr0 = new StreamReader(@"C:\SpaceY\NYTC\guess.txt");
            for (int i = 0; i < 5; i++)
            {
                for (int j = 0; j < 5; j++)
                {
                    a[i, j].Text = ((char)sr0.Read()).ToString();
                }
            }
            sr0.Close();

            try
            {
                StreamReader sr1 = new StreamReader(@"C:\SpaceY\NYTC\eventLog.txt");
                FolderView.Items.Clear();
                while (sr1.Peek() > 0)
                {
                    var item = new TreeViewItem();
                    item.Header = sr1.ReadLine();
                    FolderView.Items.Add(item);
                }
                sr1.Close();
            }
            catch (Exception E)
            {
                Console.WriteLine("Exception caugth {0}", exceptionNumber++);
            }

            /*
            while (true)
            {
                System.Threading.Thread.Sleep(1000);
            }
            */
        }

        private void Show_Solution(object sender, RoutedEventArgs e)
        {
            Solution s = new Solution(ref sol);
            s.Left = Left + Width * 3 / 4;
            s.Top = Top + Height / 6;
            s.Show();
        }
    }
}
