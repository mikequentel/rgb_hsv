import sys
import math

def toDegrees(raw_value):
  return int(raw_value * 360)

def fromDegrees(degrees_value):
  return float(degrees_value/360.0)

def toRoundedPercentage(raw_value):
  return int(round(raw_value * 100))

def fromPercentage(percent_value):
  return float(percent_value * 0.01)

def from8bit(bit_value):
  return float(bit_value/256.0)

def to8bit(raw_value):
  return int(round(raw_value * 256))

def rgb2hsv(R, G, B):
  print "Start of rgb2hsv()"

  if R == G == B == 0.0:
    return {'h':0, 's':0, 'v':0}

  # DETERMINES MAXIMUM RGB VALUE "V" WHICH IS A MEASURE OF THE DEPARTURE
  # FROM BLACK.
  V = max(R, G, B)

  # DETERMINES MININUM RGB VALUE "X".
  X = min(R, G, B)

  # DETERMINES SATURATION "S".
  S = (V - X)/V

  # DETERMINES ADJUSTED RED, GREEN, BLUE VALUES "r", "g", "b".
  r = (V - R)/(V - X)
  g = (V - G)/(V - X)
  b = (V - B)/(V - X)

  # DETERMINES HUE "H"
  H = 0
  if R == V:
    H = G == X and 5 + b or 1 - g
  if G == V:
    H = B == X and 1 + r or 3 -b
  else:
    H = R == X and 3 + g or 5 - r
  H /= 6.0

  hue = toDegrees(H)
  saturation = toRoundedPercentage(S)
  value = toRoundedPercentage(V)

  return {'h':hue, 's':saturation, 'v':value}

def hsv2rgb(H, S, V):
  print "Start of hsv2rgb()"

  if H == S == V == 0.0:
    return {'r':0, 'g':0, 'b':0}

  H *= 6
  I = math.floor(H)
  F = H - I
  M = V * (1 - S)
  N = V * (1 - S * F)
  K = V * (1 - S * (1 - F))

  R = G = B = 0.0
  if I == 0:
    R = V
    G = K
    B = M
  elif I == 1:
    R = N
    G = V
    B = M
  elif I == 2:
    R = M
    G = V
    B = K
  elif I == 3:
    R = M
    G = N
    B = V
  elif I == 4:
    R = K
    G = M
    B = V
  else:
    R = V
    G = M
    B = N

  red = to8bit(R)
  green = to8bit(G)
  blue = to8bit(B)

  return {'r':red, 'g':green, 'b':blue}

def lambda_handler(event, context):

  # TEST VALUE: mint-green:
  # red, green, blue: 36, 174, 133
  # HSV: 162, 79, 68

  # defaults
  rgb = None
  hsv = None
  red = None
  green = None
  blue = None
  hue = None
  saturation = None
  value = None

  if event.has_key('red'):
    red = int(event['red'])
  if event.has_key('green'):
    green = int(event['green'])
  if event.has_key('blue'):
    blue = int(event['blue'])

  if event.has_key('hue'):
    hue = int(event['hue'])
  if event.has_key('saturation'):
    saturation = int(event['saturation'])
  if event.has_key('value'):
    value = int(event['value'])

  if red is not None:
    R = from8bit(red)
  if green is not None:
    G = from8bit(green)
  if blue is not None:
    B = from8bit(blue)
    hsv = rgb2hsv(R, G, B)

  if hue is not None:
    H = fromDegrees(hue)
  if saturation is not None:
    S = fromPercentage(saturation)
  if value is not None:
    V = fromPercentage(value)
    rgb = hsv2rgb(H, S, V)

  return {"statusCode": 200,"headers":{"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},"body":[rgb, hsv]}
