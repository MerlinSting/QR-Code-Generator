import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer, SquareModuleDrawer, VerticalBarsDrawer, RoundedModuleDrawer, HorizontalBarsDrawer, GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import ImageColorMask, SolidFillColorMask, RadialGradiantColorMask, SquareGradiantColorMask, VerticalGradiantColorMask, HorizontalGradiantColorMask

def qr_maker(data, version=5, ec="H", box_size=10, border=4):
    """Creates the qr code based on the set parameters

    Args:
        data (any): Data to be encoded as a QR code
        version (int, optional): Size of QR code relative to image size. Defaults to 5.
        ec (str, optional): Error correction. Defaults to "H".
        box_size (int, optional): Size of each box in the QR code in pixels. Defaults to 10.
        border (int, optional): Size of border in boxes. Defaults to 4.

    Returns:
        QR: Returns QRCode object (from qrcode module). Requires qr_basic or qr_styler to be exported
    """
    if ec == "H": 
        error = qrcode.constants.ERROR_CORRECT_H
    elif ec == "Q": 
        error = qrcode.constants.ERROR_CORRECT_Q
    elif ec == "M": 
        error = qrcode.constants.ERROR_CORRECT_M
    elif ec == "L": 
        error = qrcode.constants.ERROR_CORRECT_L
    
    qr = qrcode.QRCode(
        version = version, # size, 1-40
        error_correction = error,
        box_size = box_size,
        border = border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr

def qr_basic(qr, fill="black", back="white"):
    img = qr.make_image(fill_color=fill, back_color=back)
    return img

def qr_styler(qr, fill=(0,0,0), back=(255,255,255), other=(0,0,0), path="images\\QR Code Generator\\scan_me.png", 
            colormask=0, moduledrawer=0, embed=False):
    match colormask:
        case 0: mask=SolidFillColorMask(back_color=back, front_color=fill)
        case 1: mask=RadialGradiantColorMask(back_color=back, center_color=fill, edge_color=other)
        case 2: mask=SquareGradiantColorMask(back_color=back, center_color=fill, edge_color=other)
        case 3: mask=HorizontalGradiantColorMask(back_color=back, left_color=fill, right_color=other)
        case 4: mask=VerticalGradiantColorMask(back_color=back, top_color=fill, bottom_color=other)
        case 5: mask=ImageColorMask(back_color=back, color_mask_path=path)
    match moduledrawer:
        case 0: drawer=SquareModuleDrawer()
        case 1: drawer=GappedSquareModuleDrawer()
        case 2: drawer=CircleModuleDrawer()
        case 3: drawer=RoundedModuleDrawer()
        case 4: drawer=VerticalBarsDrawer()
        case 5: drawer=HorizontalBarsDrawer()
    if embed == True:
        img = qr.make_image(image_factory = StyledPilImage, color_mask=mask, module_drawer=drawer, embeded_image_path=path)
    else:
        img = qr.make_image(image_factory = StyledPilImage, color_mask=mask, module_drawer=drawer)
    
    return img

# To export use save_image from subfunctions
    
def main():
    # qr = qr_maker("Try")
    # img = qr_basic(qr)
    #img = qr_styler(qr)
    # print(img.__dict__['_img'])
    # img.save("temp.png")
    pass

if __name__ == "__main__":
    main()