using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Space_Y
{
    class TextBoxContent : INotifyPropertyChanged
    {
        string text;
        public string Text { get { return text; } set { text = value; OnPropertyChanged("Text"); } }

        public TextBoxContent()
        {
            text = "";
        }

        public TextBoxContent(string s)
        {
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
