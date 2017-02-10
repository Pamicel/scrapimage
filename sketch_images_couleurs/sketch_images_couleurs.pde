// ------------------------------------
import codeanticode.syphon.*;
import toxi.color.*;
import toxi.math.*;
import java.util.*;
import java.nio.file.*;
import java.io.InputStreamReader;
import static java.nio.file.StandardWatchEventKinds.*;

// ------------------------------------
boolean __DEBUG__ = true;
float COLUMN_SPEED = 100;
int COLUMN_NB_COLORS = 6;
float COLUMN_TOLERANCE_COLORS = 0.1;


// ------------------------------------
ArrayList<ColumnColor> columns;
SyphonServer server;


// ------------------------------------
void settings() 
{
  size(400, 400, P3D);
  PJOGL.profile=1;
}

// ------------------------------------
void setup() 
{
  server = new SyphonServer(this, "Processing Syphon");

  columns = new ArrayList<ColumnColor>();
  columns.add( new ColumnColor("data/instagram/", 0, 0, width/3, height) );
  columns.add( new ColumnColor("data/pinterest/", width/3, 0, width/3, height) );
  columns.add( new ColumnColor("data/Tumblr/", 2*width/3, 0, width/3, height) );

  for (ColumnColor column : columns)
    column.start();

  // Debug only
  //ScrapImages testScrap = new ScrapImages("python3 /Users/paulamicel/PycharmProjects/shitty_scrapers/sketch_images_couleurs/scrapers.py");
  //testScrap.run();
}

// ------------------------------------
void draw() 
{
  background(0);

  for (ColumnColor column : columns)
  {
    column.update();
    column.draw();
  }

  server.sendScreen();
}