#!/usr/bin/env python

# Poster Creation in GIMP Python

from gimpfu import *

def poster(file1, file2, file3, file4, text, fontsize, font, colorBack, colorFore, applyOilify, saturation_level):
    # Make a new image. Size 1200x800.
    imgW, imgH = 2480, 3508
    img = gimp.Image(imgW, imgH, RGB)
    gimp.message("Created a new image")

    # Make the colors
    pdb.gimp_context_set_background(colorBack)
    pdb.gimp_context_set_foreground(colorFore)
    gimp.message("Created colors")

    # Make a background layer
    background = gimp.Layer(img, "background", imgW, imgH, RGB_IMAGE, 100, NORMAL_MODE)
    background.fill(BACKGROUND_FILL)
    img.add_layer(background, 1)
    gimp.message("Created background")

    # Make a new text layer for the writer
    textLayer = pdb.gimp_text_fontname(img, None, imgW/2, imgH*5/6, text, 10, True, fontsize, PIXELS, font)
    textLayer.translate(-textLayer.width/2, -textLayer.height/2)
    pdb.gimp_text_layer_set_color(textLayer, colorFore)
    gimp.message("Created text")

    # Make a new text layer for the title
    layer = pdb.gimp_text_fontname(img, None, imgW/2, imgH/8, "To THE LIGHTHOUSE", 10,
                                   True, 210, PIXELS, 'Copperplate Bold')
    layer.translate(-layer.width/2, -layer.height/2)
    pdb.gimp_text_layer_set_color(layer, colorFore)
    gimp.message("text layer created")

    # Make image layer 1 for the skull
    image1 = pdb.file_png_load(file1, file1)
    pdb.gimp_edit_copy(image1.layers[0])
    imageLayer1 = gimp.Layer(img, "image 1",image1.width, image1.height, RGBA_IMAGE, 100, NORMAL_MODE)
    img.add_layer(imageLayer1,1)
    floatingLayer = pdb.gimp_edit_paste(imageLayer1, True)
    pdb.gimp_floating_sel_anchor(floatingLayer)
    imageLayer1.translate((imgW - imageLayer1.width) / 2, (imgH - imageLayer1.height) / 2)

    # Add Oilify effect
    if applyOilify:
        pdb.plug_in_oilify(img, imageLayer1, 60, 1)

    # Make image layer 2 for the lighthouse
    image2 = pdb.file_png_load(file2, file2)
    pdb.gimp_edit_copy(image2.layers[0])
    imageLayer2 = gimp.Layer(img, "image 2", image2.width, image2.height, RGBA_IMAGE, 100, NORMAL_MODE)
    img.add_layer(imageLayer2,1)
    floatingLayer = pdb.gimp_edit_paste(imageLayer2, True)
    pdb.gimp_floating_sel_anchor(floatingLayer)
    imageLayer2.translate((imgW - imageLayer2.width) / 2, (imgH - imageLayer2.height) / 2)

    # Add a wind filter fot img2 the lighthouse
    pdb.plug_in_wind(img, imageLayer2, 10, 1, 10, 0, 0)
  
    # Make image layer 3 for the windows
    image3 = pdb.file_png_load(file3, file3)
    pdb.gimp_edit_copy(image3.layers[0])
    imageLayer3 = gimp.Layer(img, "image 3", image3.width, image3.height, RGBA_IMAGE, 100, NORMAL_MODE)
    img.add_layer(imageLayer3,1)
    floatingLayer = pdb.gimp_edit_paste(imageLayer3, True)
    pdb.gimp_floating_sel_anchor(floatingLayer)
    imageLayer3.translate(imgW / 8 + imageLayer3.width, (imgH - imageLayer3.height) / 2)


    # Duplicate imageLayer3 to make a window on the right
    imageLayer3_copy = imageLayer3.copy()
    imageLayer3_copy.name = "image 3 copy"
    img.add_layer(imageLayer3_copy, 0)

    # Mirror the duplicated layer horizontally
    pdb.gimp_item_transform_flip_simple(imageLayer3_copy, ORIENTATION_HORIZONTAL, True, 0)

    # Move the new layer(right window) to the symmetrical position 
    imageLayer3_copy.translate(imgW/4*3-imageLayer3.width*3, 0)

    

    # Make image layer 4 for the flowers
    image4 = pdb.file_png_load(file4, file4)
    pdb.gimp_image_scale(image4, imgW/6, imgH/7)
    pdb.gimp_edit_copy(image4.layers[0])
    imageLayer4 = gimp.Layer(img, "image 4", imgW/6, imgH/6, RGBA_IMAGE, 100, NORMAL_MODE)
    img.add_layer(imageLayer4,1)
    floatingLayer = pdb.gimp_edit_paste(imageLayer4, True)
    pdb.gimp_floating_sel_anchor(floatingLayer)
    imageLayer4.translate((imgW - imageLayer4.width) / 2, imgH / 7 * 6 )

    # Adjust the saturation of the entire image
    for layer in img.layers:
        pdb.gimp_hue_saturation(layer, HUE_RANGE_ALL, 0, 0, saturation_level)


    # Create a new image window
    gimp.Display(img)
    # Show the new image window
    gimp.displays_flush()

register(
    "python_fu_poster",
    "To The Lighthouse Poster",
    "Create a custom poster with four images",
    "LW",
    "Copyright@LW",
    "2023",
    "To The Lighthouse Poster",
    "", # Create a new image, don't work on an existing one
    [
        (PF_FILE, "file1", "Choose Image 1", ""),
        (PF_FILE, "file2", "Choose Image 2", ""),
        (PF_FILE, "file3", "Choose Image 3", ""),
        (PF_FILE, "file4", "Choose Image 4", ""),
        (PF_STRING, "text", "Enter Text", "Virginia Woolf"),
        (PF_SPINNER, "fontsize", "Font Size", 100, (10, 200, 5)),
        (PF_FONT, "font", "Choose Font", "Copperplate"),
        (PF_COLOR, "colorBack", "Background color", (255, 247, 225)),
        (PF_COLOR, "colorFore", "Foreground color", (0, 0, 0)),
        (PF_TOGGLE, "applyOilify", "Apply Oilify to Image 1", False),#turn on/off the oilify effect on image1
        (PF_SLIDER, "saturation_level", "Saturation Level", 0, (-100, 100, 1)),# customise the saturation of the poster
        
    ],
    [],
    poster,
    menu="<Image>/File/Create/Assign2"
)

main()
