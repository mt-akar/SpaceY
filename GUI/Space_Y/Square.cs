using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;

namespace Space_Y
{
    public class Square : INotifyPropertyChanged
    {
        int row;
        public int Row { get { return row; } set { row = value; } }

        int column;
        public int Column { get { return column; } set { column = value; } }

        string text;
        public string Text { get { return text; } set { text = value; OnPropertyChanged("Text"); } }

        string referanceNumber;
        public string ReferanceNumber { get { return referanceNumber; } set { referanceNumber = value; } }

        SolidColorBrush backgroundColor;
        public SolidColorBrush BackgroundColor { get { return backgroundColor; } set { backgroundColor = value; } }

        public Square(int r, int c, string rf, Color bg)
        {
            row = r;
            column = c;
            text = "";
            referanceNumber = rf;
            backgroundColor = new SolidColorBrush();
            BackgroundColor.Color = bg;
        }

        public Square(int r, int c, string s)
        {
            row = r;
            column = c;
            text = s;
        }

        public event PropertyChangedEventHandler PropertyChanged;
        public void OnPropertyChanged(string property)
        {
            if (PropertyChanged != null)
                PropertyChanged(this, new PropertyChangedEventArgs(property));
        }
    }
}
