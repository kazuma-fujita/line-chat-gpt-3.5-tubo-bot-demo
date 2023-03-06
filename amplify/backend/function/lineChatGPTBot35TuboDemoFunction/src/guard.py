import hashlib
import hmac
import base64
import const


def verify_request(event):
    """
    Verify the authenticity of the incoming webhook request from LINE platform by comparing the signature in the request header
        with the signature generated using LINE Channel Secret.

    Parameters:
        event (dict): Dictionary representing the incoming webhook event data, which includes the headers and the body of the request.

    Returns:
        None

    Raises:
        Exception: If the request signature from the headers does not match the signature generated using LINE Channel Secret.
    """
    x_line_signature = event["headers"].get("x-line-signature") or event["headers"].get("X-Line-Signature")
    body = event["body"]

    # Generate the signature using HMAC-SHA256
    hash = hmac.new(const.LINE_CHANNEL_SECRET.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)

    # Compare the signature from the request headers with the generated signature
    if signature != x_line_signature.encode():
        raise Exception("Request verification failed. Request came from a non-LINE server source.")
