using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
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
        private string resultFolder = "E:/Project/c#";
        private int imageCounter = 1;
        private List<(int x, int y, int w, int h)> detectedRectangles = new List<(int x, int y, int w, int h)>();

        public Form1()
        {
            InitializeComponent();
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

                            // Process rectangles and save images
                            ProcessRectangles();

                            Cv2.WaitKey(10);
                        }
                    }
                }
            });
        }
        CascadeClassifier faceCascade = new CascadeClassifier("E:/Project/object_detection/data/model/cascade.xml");

        private void ProcessRectangles()
        {
            Mat frameCopy = _image.Clone();

            // Convert the Mat to grayscale for better performance in object detection
            Mat gray = new Mat();
            Cv2.CvtColor(frameCopy, gray, ColorConversionCodes.BGR2GRAY);

            double scaleFactor = 6;
            int minNeighbors = 8;
            Size minSize = new Size(30, 30);

            Rect[] objects = faceCascade.DetectMultiScale(gray, scaleFactor, minNeighbors);


            // Clear the list of detected rectangles
            detectedRectangles.Clear();

            // Draw rectangles on the frame and add them to the list
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


        // Python code translated to C# for image preprocessing
private void PreprocessImages()
{
                foreach (var imgPath in Directory.GetFiles(resultFolder))
        {
            Console.WriteLine($"Preprocessed gwa");

            Mat img = Cv2.ImRead(imgPath);
            Mat preprocessedImg = PreprocessImage(img);

            string outputClassDirectory = Path.Combine(@"E:/Project/c#/preproc", Path.GetFileName(imgPath));

                preprocessedImg.SaveImage(outputClassDirectory);

    }
}

        // Python code translated to C# for image preprocessing
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
        private void button1_Click(object sender, EventArgs e)
        {
            Console.WriteLine($"#rectangles: {detectedRectangles.Count}");

            // Create a copy of the list to avoid the 'Collection was modified' exception
            List<(int x, int y, int w, int h)> rectanglesCopy = new List<(int x, int y, int w, int h)>(detectedRectangles);

            foreach (var (x, y, w, h) in rectanglesCopy)
            {
                Mat frameCopy = _image.Clone();
                Mat croppedImage = new Mat(frameCopy, new Rect(x, y, w, h));

                // Generate a unique identifier for the image
                string uniqueIdentifier = Guid.NewGuid().ToString();
                string imagePath = Path.Combine(resultFolder, $"object_{uniqueIdentifier}.png");

                croppedImage.SaveImage(imagePath);

                // Add the unique identifier to the list instead of using imageCounter
                listBox1.Items.Add($"object_{uniqueIdentifier}");

                // Remove the processed rectangle from the original list
                detectedRectangles.Remove((x, y, w, h));
            }

            // Additional logic after preprocessing...
            PreprocessImages();
            CallPythonScriptForPredictions();
            // Print the count after removing processed rectangles
            Console.WriteLine($"#remaining rectangles: {detectedRectangles.Count}");
        }

        private void CallPythonScriptForPredictions()
        {
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

                // Process the output (predicted labels)
                string[] predictedLabels = output.Split(',');
                foreach (string label in predictedLabels)
                {
                    Console.WriteLine($"Predicted Label: {label}");
                }
                // Display the predicted labels in your C# application
                // For example, update a label or list box with the predicted labels
            }
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

        private void listBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

    }
}
