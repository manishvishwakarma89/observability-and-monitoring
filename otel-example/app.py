import logging
from random import randint

from flask import Flask, jsonify, request

from opentelemetry import metrics, trace

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("rolldice")

# Custom telemetry. The opentelemetry-instrument wrapper configures the
# exporters, so the app only asks for a tracer and a meter.
tracer = trace.get_tracer("rolldice.tracer")
meter = metrics.get_meter("rolldice.meter")
roll_counter = meter.create_counter(
    "dice.rolls", description="Number of dice rolls, by roll value"
)

app = Flask(__name__)


def roll(sides):
    with tracer.start_as_current_span("roll") as span:
        result = randint(1, sides)
        span.set_attribute("roll.sides", sides)
        span.set_attribute("roll.value", result)
        roll_counter.add(1, {"roll.value": result})
        return result


@app.route("/")
def index():
    return jsonify(message="Try /rolldice?player=Alice&sides=6")


@app.route("/rolldice")
def roll_dice():
    player = request.args.get("player", default="anonymous", type=str)
    sides = request.args.get("sides", default=6, type=int)

    if not 2 <= sides <= 100:
        logger.warning("%s asked for an invalid dice size: %s", player, sides)
        return jsonify(error="sides must be between 2 and 100"), 400

    result = roll(sides)
    logger.info("%s rolled a d%s and got %s", player, sides, result)
    return jsonify(player=player, sides=sides, roll=result)


@app.route("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
