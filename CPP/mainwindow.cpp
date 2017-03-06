#include "mainwindow.h"
#include "ui_mainwindow.h"


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow){
    ui->setupUi(this);
}

MainWindow::~MainWindow(){
    delete ui;
}

void MainWindow::on_pushButton_clicked(){

   QString fName = QFileDialog::getOpenFileName(this,
                                                tr("Open Image"),".",
                                                tr("Image Files (*.png *.jpg *.jpeg *.bmp)"));


   image = cv::imread(fName.toStdString());
   cv::namedWindow("Original Image");
   cv::imshow("Original Image", image);
}

void MainWindow::on_pushButton_2_clicked(){
   cv::flip(image,image,1);
   // change color channel ordering
   cv::cvtColor(image,image,CV_BGR2RGB);

   QImage img ((const unsigned char*)(image.data),
                       image.cols, image.rows, QImage::Format_RGB888);


   //display on label
   ui->label->setPixmap(QPixmap::fromImage(img));

   //resize label
   ui->label->resize(ui->label->pixmap()->size());
}
