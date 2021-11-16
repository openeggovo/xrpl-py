from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.it_utils import test_async_and_sync
from tests.integration.reusable_values import WALLET
from xrpl.asyncio.clients.utils import (
    json_to_response,
    request_to_json_rpc,
    request_to_websocket,
    websocket_to_response,
)
from xrpl.asyncio.transaction import (
    safe_sign_and_autofill_transaction as safe_sign_and_autofill_transaction_async,
)
from xrpl.core.binarycodec import encode
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.requests import SubmitOnly
from xrpl.models.transactions import OfferCreate

TX = OfferCreate(
    account=WALLET.classic_address,
    sequence=WALLET.sequence,
    last_ledger_sequence=WALLET.sequence + 10,
    taker_gets="13100000",
    taker_pays=IssuedCurrencyAmount(
        currency="USD",
        issuer=WALLET.classic_address,
        value="10",
    ),
)


class TestSubmitOnly(IntegrationTestCase):
    @test_async_and_sync(globals())
    async def test_basic_functionality(self, client):
        transaction = await safe_sign_and_autofill_transaction_async(TX, WALLET, client)
        tx_json = transaction.to_xrpl()
        tx_blob = encode(tx_json)
        response = await client.request(
            SubmitOnly(
                tx_blob=tx_blob,
            )
        )
        self.assertTrue(response.is_successful())

    @test_async_and_sync(globals())
    async def test_request_json(self, client):
        # TODO: run request_json tests via metaprogramming, instead of copy-paste
        transaction = await safe_sign_and_autofill_transaction_async(TX, WALLET, client)
        tx_json = transaction.to_xrpl()
        tx_blob = encode(tx_json)
        is_websocket = "ws" in client.url
        req = SubmitOnly(
            tx_blob=tx_blob,
        )
        if is_websocket:
            request = request_to_websocket(req)
        else:
            request = request_to_json_rpc(req)
        response = await client.request_json(request)
        if is_websocket:
            resp = websocket_to_response(response)
        else:
            resp = json_to_response(response)
        self.assertTrue(resp.is_successful())
