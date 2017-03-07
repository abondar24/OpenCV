#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include<QImage>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <QFileDialog>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    void salt(cv::Mat &image, int n);
    void colorReduce(cv::Mat &image, int div =64);
    void colorReduce(cv::Mat &image,cv::Mat &result, int div=64);
    void colorReduceIter(cv::Mat &image, int div =64);
    void sharpen(cv::Mat &image,cv::Mat &result);
    void sharpen2D(cv::Mat &image,cv::Mat &result);
    void roiDemo(cv::Mat &image);


    ~MainWindow();

private slots:
    void on_pushButton_clicked();

    void on_pushButton_2_clicked();

    void on_pushButton_3_clicked();

    void on_pushButton_4_clicked();

    void on_pushButton_5_clicked();

    void on_pushButton_6_clicked();

    void on_pushButton_7_clicked();

    void on_pushButton_8_clicked();

private:
    Ui::MainWindow *ui;
    cv::Mat image;
    void displayImage(cv::Mat &image);

};

#endif // MAINWINDOW_H
