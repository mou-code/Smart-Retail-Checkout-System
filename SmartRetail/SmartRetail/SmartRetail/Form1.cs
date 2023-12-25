using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Printing;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Threading.Tasks;
using System.Windows.Forms;
using OpenCvSharp;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.Window;
using Point = OpenCvSharp.Point;
using Size = OpenCvSharp.Size;

namespace SmartRetail
{

    public partial class Form1 : Form
    {
        private Mat _image = new Mat();
        //Replace these pathes with your own
        private string currentProcess_framesReceipt = "E:/ip_output/current_process";
        private string currentProcess_croppedImages = "E:/ip_output/current_process/cropped_images";
        private string currentProcess_preprocessedImages = "E:/ip_output/current_process/preprocessed_images";
        private string currentProcess_croppedImagesDone = "E:/ip_output/current_process/done/cropped_images";
        private string currentProcess_preprocessedImagesDone = "E:/ip_output/current_process/done/preprocessed_images";

        private Stopwatch detectionStopwatch = new Stopwatch();
        private Stopwatch preprocessingStopwatch = new Stopwatch();
        private Stopwatch classificationStopwatch = new Stopwatch();


        private List<(int x, int y, int w, int h)> detectedRectangles = new List<(int x, int y, int w, int h)>();

        public Form1()
        {

            InitializeComponent();
            listBox1.MouseDoubleClick += listBox1_MouseDoubleClick;

            // Set the DrawMode to OwnerDrawFixed to handle the drawing of items
            listBox1.DrawMode = DrawMode.OwnerDrawFixed;
            listBox1.DataSource = productList;
            listBox1.SelectedIndex = -1;
            listBox1.DrawItem += listBox1_DrawItem;
            UpdateTotalLabel();

        }

        [DllImport("user32.DLL", EntryPoint = "ReleaseCapture")]
        private extern static void ReleaseCapture();
        [DllImport("user32.DLL", EntryPoint = "SendMessage")]
        private extern static void SendMessage(System.IntPtr one, int two, int three, int four);
        
        private void Form1_Load(object sender, EventArgs e)
        {
            RunCamera();
        }

        void RunCamera()
        {
            Task.Run(() =>
            {
                using (var capture = new VideoCapture(3))
                {
                    capture.Set(capture.FrameWidth, 700);
                    capture.Set(capture.FrameHeight, 700);
                    {
                        while (true)
                        {
                            _image = capture.RetrieveMat();
                            if (_image.Empty())
                                break;

                            Bitmap bitmap = OpenCvSharp.Extensions.BitmapConverter.ToBitmap(_image);

                            pictureBox1.BeginInvoke(new Action(() =>
                            {
                                pictureBox1.Image = bitmap;
                                pictureBox1.Refresh();
                            }));
                            detectionStopwatch.Restart();
                            ProcessRectangles();
                            detectionStopwatch.Stop();

                            Cv2.WaitKey(10);
                        }
                    }
                }
            });
        }
        //Replace with your own model
        CascadeClassifier detectionModel = new CascadeClassifier("E:/Project/object_detection/data/model/cascade.xml");

        private void ProcessRectangles()
        {
            Mat frameCopy = _image.Clone();
            Mat gray = new Mat();
            Cv2.CvtColor(frameCopy, gray, ColorConversionCodes.BGR2GRAY);

            double scaleFactor = 6;
            int minNeighbors = 8;
            Size minSize = new Size(30, 30);

            Rect[] objects = detectionModel.DetectMultiScale(gray, scaleFactor, minNeighbors);

            detectedRectangles.Clear();

            foreach (var rect in objects)
            {
                if(rect.Width > 30 && rect.Height > 30)
                {
                    Cv2.Rectangle(frameCopy, rect, new Scalar(255, 0, 255), 2);
                    detectedRectangles.Add((rect.X, rect.Y, rect.Width, rect.Height));
                }

            }

            pictureBox1.BeginInvoke(new Action(() =>
            {
                pictureBox1.Image = OpenCvSharp.Extensions.BitmapConverter.ToBitmap(frameCopy);
                pictureBox1.Refresh();
            }));

        }

        private int framecounter = 1;

        private void button1_Click(object sender, EventArgs e)
        {
            Console.WriteLine("Starting the process");
            Mat currentFrame = _image.Clone();

            currentFrame.SaveImage(Path.Combine(currentProcess_framesReceipt, $"frame{framecounter}.png"));
            framecounter++;

            // Create a copy of the list to avoid the 'Collection was modified' exception
            List<(int x, int y, int w, int h)> rectanglesCopy = new List<(int x, int y, int w, int h)>(detectedRectangles);

            foreach (var (x, y, w, h) in rectanglesCopy)
            {
                Mat frameCopy = _image.Clone();
                Mat croppedImage = new Mat(frameCopy, new Rect(x, y, w, h));
                string uniqueIdentifier = Guid.NewGuid().ToString();
                string imagePath = Path.Combine(currentProcess_croppedImages, $"object_{uniqueIdentifier}.png");

                croppedImage.SaveImage(imagePath);

                detectedRectangles.Remove((x, y, w, h));
            }
            Console.WriteLine("Done: Cropping the detections");
            preprocessingStopwatch.Restart();
            PreprocessImages();
            preprocessingStopwatch.Stop();

            Console.WriteLine("Done: Preprocessing the cropped images");

            classificationStopwatch.Restart();
            List<string> predictedLabels = GetPredictedLabels();
            classificationStopwatch.Stop();

            Console.WriteLine("Done: Predicting the preprocessed images");

            if (detectedRectangles.Count > 0)
            {
                foreach (string label in predictedLabels)
                {
                    Console.WriteLine("Label: " + label);

                    switch (label.ToLower().Trim())
                    {
                        case "latief":
                            Console.WriteLine("Adding Latief Tea");
                            productList.Add(new ProductItem
                            {
                                ProductName = "Latief Tea - 250g",
                                Counter = 1,
                                Price = 46.75M
                            });
                            break;

                        case "pasta":
                            Console.WriteLine("Adding Cairo Pasta");
                            productList.Add(new ProductItem
                            {
                                ProductName = "Cairo Pasta - 400g",
                                Counter = 1,
                                Price = 10.25M
                            });
                            break;

                        case "lipton":
                            Console.WriteLine("Adding Lipton Mint Tea");
                            productList.Add(new ProductItem
                            {
                                ProductName = "Lipton Mint Tea - 20 Sachets",
                                Counter = 1,
                                Price = 40.32M
                            });
                            break;

                        case "zaza":
                            Console.WriteLine("Adding Zaza Oil");
                            productList.Add(new ProductItem
                            {
                                ProductName = "Zaza Oil - 700ml",
                                Counter = 1,
                                Price = 41.95M
                            });
                            break;

                        case "sugar":
                            Console.WriteLine("Adding Aunty Baheya Sugar");
                            productList.Add(new ProductItem
                            {
                                ProductName = "Aunty Baheya Sugar - 1kg",
                                Counter = 1,
                                Price = 28M
                            });
                            break;

                        case "basmati":
                            Console.WriteLine("Adding Rehana Basmati");
                            productList.Add(new ProductItem
                            {
                                ProductName = "Rehana Basmati - 1kg",
                                Counter = 1,
                                Price = 69.95M
                            });
                            break;

                        default:
                            Console.WriteLine("Unknown label: " + label);
                            break;
                    }
                }

                listBox1.DataSource = null;
                listBox1.DataSource = productList;

                UpdateTotalLabel();
                MoveImagesToDoneFolder(currentProcess_croppedImages, currentProcess_croppedImagesDone);
                Console.WriteLine("Done: Moving cropped images to 'done' folder");

                MoveImagesToDoneFolder(currentProcess_preprocessedImages, currentProcess_preprocessedImagesDone);
                Console.WriteLine("Done: Moving processed images to 'done' folder");

                string performanceFilePath = Path.Combine("E:/ip_output/current_process", "performance_log.txt");
                using (StreamWriter writer = new StreamWriter(performanceFilePath, true))
                {
                    writer.WriteLine($"Detection Time: {detectionStopwatch.ElapsedMilliseconds} ms");
                    writer.WriteLine($"Preprocessing Time: {preprocessingStopwatch.ElapsedMilliseconds} ms");
                    writer.WriteLine($"Classification Time: {classificationStopwatch.ElapsedMilliseconds} ms");
                    writer.WriteLine();
                }


            }

        }

        private void UpdateTotalLabel()
        {
            decimal total = productList.Sum(item => item.Price * item.Counter);
            label_total.Text = $"{total}";
        }


        private void MoveImagesToDoneFolder(string sourceFolderPath, string doneFolderPath)
        {
            try
            {
                foreach (var filePath in Directory.GetFiles(sourceFolderPath))
                {
                    string fileName = Path.GetFileName(filePath);
                    string destinationPath = Path.Combine(doneFolderPath, fileName);

                    File.Move(filePath, destinationPath);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error moving images: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }


        private List<string> GetPredictedLabels()
        {
            var predictedLabels = new List<string>();

            var processInfo = new ProcessStartInfo
            {
                FileName = "python",
                Arguments = "lab_class_predict.py",
                RedirectStandardInput = false,
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using (var process = new Process { StartInfo = processInfo })
            {
                process.Start();
                string output = process.StandardOutput.ReadToEnd();
                process.WaitForExit();

                predictedLabels.AddRange(output.Split(','));
            }

            return predictedLabels;
        }

        private void PreprocessImages()
        {
            foreach (var imgPath in Directory.GetFiles(currentProcess_croppedImages))
            {
                Mat img = Cv2.ImRead(imgPath);
                Mat preprocessedImg = PreprocessImage(img);

                string outputClassDirectory = Path.Combine(currentProcess_preprocessedImages, Path.GetFileName(imgPath));

                preprocessedImg.SaveImage(outputClassDirectory);

            }
        }
        private Mat PreprocessImage(Mat img)
        {
            Mat labImg = new Mat();
            Cv2.CvtColor(img, labImg, ColorConversionCodes.BGR2Lab);

            Mat[] labChannels = Cv2.Split(labImg);
            Cv2.EqualizeHist(labChannels[0], labChannels[0]);

            Mat labImgEq = new Mat();
            Cv2.Merge(labChannels, labImgEq);

            Mat imgEq = new Mat();
            Cv2.CvtColor(labImgEq, imgEq, ColorConversionCodes.Lab2BGR);

            Mat bilateralImage = new Mat();
            Cv2.BilateralFilter(imgEq, bilateralImage, 20, 100, 70);


            return bilateralImage;
        }


        private void panel1_MouseDown(object sender, MouseEventArgs e)
        {
            ReleaseCapture();
            SendMessage(Handle, 0x112, 0xf012, 0);
        }

        private void button3_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }
        public class ProductItem
        {
            public int Counter { get; set; }
            public string ProductName { get; set; }
            public decimal Price { get; set; }
        }

        private List<ProductItem> productList = new List<ProductItem>();

        private void listBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
       

        }

        private void listBox1_MouseDoubleClick(object sender, MouseEventArgs e)
        {
            int index = listBox1.IndexFromPoint(e.Location);
            if (index != ListBox.NoMatches)
            {
                ProductItem selectedProduct = productList[index];

                using (QuantityForm quantityForm = new QuantityForm())
                {
                    quantityForm.ProductName = selectedProduct.ProductName;
                    quantityForm.NumericUpDownControl.Value = selectedProduct.Counter;

                    if (quantityForm.ShowDialog() == DialogResult.OK)
                    {
                        selectedProduct.Counter = quantityForm.SelectedQuantity;
                        listBox1.Invalidate();
                    }
                }
            }
            UpdateTotalLabel();

        }



        private void listBox1_DrawItem(object sender, DrawItemEventArgs e)
        {
            if (e.Index >= 0)
            {
                e.DrawBackground();
                ProductItem productItem = productList[e.Index];

                // Determine the text color based on the selection state
                Brush textBrush = ((e.State & DrawItemState.Selected) == DrawItemState.Selected) ? SystemBrushes.HighlightText : SystemBrushes.GrayText;

                // Draw the counter
                string counterText = $"{productItem.Counter}";
                e.Graphics.DrawString(counterText, e.Font, textBrush, e.Bounds.Left, e.Bounds.Top);

                // Draw the product name
                string productNameText = $"{productItem.ProductName}";
                float productNameX = e.Bounds.Left + e.Graphics.MeasureString(counterText, e.Font).Width + 10; // Add some padding
                e.Graphics.DrawString(productNameText, e.Font, textBrush, productNameX, e.Bounds.Top);

                // Draw the price
                string priceText = $"{productItem.Price}"; // C2 formats as currency
                float priceX = e.Bounds.Right - e.Graphics.MeasureString(priceText, e.Font).Width;
                e.Graphics.DrawString(priceText, e.Font, textBrush, priceX, e.Bounds.Top);

                e.DrawFocusRectangle();
            }
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void panel2_Paint(object sender, PaintEventArgs e)
        {

        }
        private void DeletePerformanceLogFile()
        {
            string performanceFilePath = Path.Combine("E:/ip_output/current_process", "performance_log.txt");

            try
            {
                if (File.Exists(performanceFilePath))
                {
                    File.Delete(performanceFilePath);
                    Console.WriteLine("Performance log file deleted successfully.");
                }
                else
                {
                    Console.WriteLine("Performance log file does not exist.");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error deleting performance log file: {ex.Message}");
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            // 1. Delete all images inside currentProcess and currentProcess_croppedImages and currentProcess_framesReceipt
            ClearImageDirectory(currentProcess_preprocessedImages);
            ClearImageDirectory(currentProcess_croppedImages);
            ClearImageDirectory(currentProcess_preprocessedImagesDone);
            ClearImageDirectory(currentProcess_croppedImagesDone);
            ClearImageDirectory(currentProcess_framesReceipt);
            DeletePerformanceLogFile();

            // 2. Delete all items in the productList and refresh the ListBox
            productList.Clear();
            listBox1.DataSource = null;
            listBox1.DataSource = productList;
            framecounter = 0;
        }
        private void ClearImageDirectory(string directoryPath)
        {
            try
            {
                // Delete all files in the specified directory
                foreach (var filePath in Directory.GetFiles(directoryPath))
                {
                    File.Delete(filePath);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error clearing directory {directoryPath}: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void panel3_Paint(object sender, PaintEventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }
        private void PrintList(object sender, PrintPageEventArgs e)
        {
            float yPos = 0;
            float leftMargin = e.MarginBounds.Left;
            float topMargin = e.MarginBounds.Top;

            foreach (ProductItem productItem in productList)
            {
                string text = $"{productItem.Counter} {productItem.ProductName} {productItem.Price:C2}";
                e.Graphics.DrawString(text, Font, Brushes.Black, leftMargin, topMargin + yPos);
                yPos += Font.GetHeight();
            }
        }
        private void button1_Click_1(object sender, EventArgs e)
        {
            // Create a bitmap to hold the screenshot
            Bitmap screenshot = new Bitmap(panel2.Width -2, panel2.Height - 100);

            // Create a Graphics object from the bitmap
            using (Graphics g = Graphics.FromImage(screenshot))
            {
                // Copy the content of the panel to the bitmap
                g.CopyFromScreen(panel2.PointToScreen(System.Drawing.Point.Empty), System.Drawing.Point.Empty, panel2.Size);
            }

            // Save the screenshot to a file (you can change the file format as needed)

            string filePath = Path.Combine(currentProcess_framesReceipt, "receipt.png");

            // Save the screenshot to the file
            screenshot.Save(filePath, System.Drawing.Imaging.ImageFormat.Png);

            string testCaseDir = GetNextTestCaseFolder();
            CopyDirectory(currentProcess_framesReceipt, testCaseDir);

        }
        private void CopyDirectory(string sourceDir, string destDir)
        {
            if (!Directory.Exists(destDir))
            {
                Directory.CreateDirectory(destDir);
            }

            foreach (string file in Directory.GetFiles(sourceDir))
            {
                string destFile = Path.Combine(destDir, Path.GetFileName(file));
                File.Copy(file, destFile);
            }

            foreach (string folder in Directory.GetDirectories(sourceDir))
            {
                string destFolder = Path.Combine(destDir, Path.GetFileName(folder));
                CopyDirectory(folder, destFolder);
            }
        }

        private string GetNextTestCaseFolder()
        {
            string testCasesDir = "E:/ip_output/test_cases";
            int folderNumber = 1;

            while (Directory.Exists(Path.Combine(testCasesDir, folderNumber.ToString())))
            {
                folderNumber++;
            }

            return Path.Combine(testCasesDir, folderNumber.ToString());
        }

    }
}
