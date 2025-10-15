import javafx.application.Application;
import javafx.application.Platform;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextInputDialog;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import javafx.stage.FileChooser;
import javafx.stage.Stage;

import org.opencv.core.*;
import org.opencv.dnn.Dnn;
import org.opencv.dnn.Net;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.videoio.VideoCapture;

import javafx.embed.swing.SwingFXUtils;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.Optional;
import javax.imageio.ImageIO;

public class FireSenseApp extends Application {

    private VideoCapture capture;
    private boolean isRunning = false;
    private ImageView imageView;
    private Net model;

    @Override
    public void start(Stage stage) {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);

        // Load YOLO ONNX model
        model = Dnn.readNetFromONNX("best.onnx");

        // Title
        Text title = new Text("🔥 Fire Detection System 🔥");
        title.setFont(Font.font("Arial", 30));
        title.setFill(Color.ORANGE);

        // Video Display
        imageView = new ImageView();
        imageView.setFitWidth(700);
        imageView.setFitHeight(400);
        imageView.setStyle("-fx-background-color: black; -fx-border-color: #333; -fx-border-radius: 10;");

        // Buttons
        Button btnCam = makeButton("Use Camera");
        Button btnUpload = makeButton("Upload Video");
        Button btnIP = makeButton("Enter IP");
        Button btnReset = makeButton("Reset", true);

        btnCam.setOnAction(e -> useCamera());
        btnUpload.setOnAction(e -> uploadVideo(stage));
        btnIP.setOnAction(e -> enterIP());
        btnReset.setOnAction(e -> resetScreen());

        HBox buttons = new HBox(15, btnCam, btnUpload, btnIP, btnReset);
        buttons.setAlignment(Pos.CENTER);

        // Layout
        BorderPane root = new BorderPane();
        root.setTop(title);
        BorderPane.setAlignment(title, Pos.CENTER);
        root.setCenter(imageView);
        root.setBottom(buttons);
        root.setStyle("-fx-padding: 20;");

        Scene scene = new Scene(root, 850, 600);
        stage.setScene(scene);
        stage.setTitle("FireSense");
        stage.show();
    }

    private Button makeButton(String text) {
        return makeButton(text, false);
    }

    private Button makeButton(String text, boolean grey) {
        Button btn = new Button(text);
        btn.setPrefHeight(40);
        btn.setStyle(
                grey ? "-fx-background-color: grey; -fx-text-fill: white; -fx-font-weight: bold; -fx-font-size: 16;"
                        : "-fx-background-color: #DC4D01; -fx-text-fill: white; -fx-font-weight: bold; -fx-font-size: 16;"
        );
        btn.setOnMouseEntered(e -> btn.setStyle("-fx-background-color: #FFA500; -fx-text-fill: white; -fx-font-weight: bold; -fx-font-size: 16;"));
        btn.setOnMouseExited(e -> btn.setStyle(
                grey ? "-fx-background-color: grey; -fx-text-fill: white; -fx-font-weight: bold; -fx-font-size: 16;"
                        : "-fx-background-color: #DC4D01; -fx-text-fill: white; -fx-font-weight: bold; -fx-font-size: 16;"
        ));
        return btn;
    }

    private void uploadVideo(Stage stage) {
        FileChooser fileChooser = new FileChooser();
        fileChooser.getExtensionFilters().add(new FileChooser.ExtensionFilter("Video Files", "*.mp4", "*.avi", "*.mov"));
        File file = fileChooser.showOpenDialog(stage);
        if (file != null) startVideo(file.getAbsolutePath());
    }

    private void useCamera() {
        startVideo("0");  // default webcam
    }

    private void enterIP() {
        TextInputDialog dialog = new TextInputDialog();
        dialog.setHeaderText("Enter IP or RTSP URL:");
        Optional<String> result = dialog.showAndWait();
        result.ifPresent(this::startVideo);
    }

    private void resetScreen() {
        isRunning = false;
        if (capture != null) capture.release();
        imageView.setImage(null);
    }

    private void startVideo(String source) {
        isRunning = false;
        if (capture != null) capture.release();

        capture = source.equals("0") ? new VideoCapture(0) : new VideoCapture(source);
        isRunning = true;

        new Thread(() -> {
            Mat frame = new Mat();
            while (isRunning && capture.read(frame)) {
                processFrame(frame);
                try { Thread.sleep(33); } catch (InterruptedException e) { e.printStackTrace(); }
            }
        }).start();
    }

    private void processFrame(Mat frame) {
        // Resize & create blob
        Mat blob = Dnn.blobFromImage(frame, 1/255.0, new Size(640, 640), new Scalar(0,0,0), true, false);
        model.setInput(blob);
        Mat output = model.forward();

        // TODO: add YOLO post-processing to draw boxes on frame

        Image fxImage = mat2Image(frame);
        Platform.runLater(() -> imageView.setImage(fxImage));
    }

    private Image mat2Image(Mat frame) {
        MatOfByte buffer = new MatOfByte();
        Imgcodecs.imencode(".bmp", frame, buffer);
        BufferedImage img = null;
        try { img = ImageIO.read(new java.io.ByteArrayInputStream(buffer.toArray())); }
        catch (Exception e) { e.printStackTrace(); }
        return SwingFXUtils.toFXImage(img, null);
    }

    public static void main(String[] args) { launch(); }
}
