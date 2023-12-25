using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SmartRetail
{
    public partial class QuantityForm : Form
    {
        public int SelectedQuantity { get; private set; }
        public string ProductName { get; set; }
        public NumericUpDown NumericUpDownControl => numericUpDown1;

        public QuantityForm()
        {
            InitializeComponent();
            Load += QuantityForm_Load;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            SelectedQuantity = (int)numericUpDown1.Value;
            DialogResult = DialogResult.OK;
            Close();
        }

        private void panel2_Paint(object sender, PaintEventArgs e)
        {

        }

        private void QuantityForm_Load(object sender, EventArgs e)
        {
            label2.Text = ProductName;
            // In the QuantityForm constructor or load event


        }
    }
}
