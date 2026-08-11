# -*- coding: utf-8 -*-
from odoo.addons.farm_core.tests.bdd_base import BddTransactionCase
from odoo.exceptions import UserError, ValidationError

class TestEpic049(BddTransactionCase):
    """ BDD Test Suite for Epic 049: Epic 049 Blockchain Biological Asset Evidence """

    def setUp(self):
        super(TestEpic049, self).setUp()

    def test_01_organic_lot_certification_hash_compilation(self):
        """
        Scenario: Organic Lot Certification Hash Compilation
        Given a completed organic grain harvest lot "GRAIN-LOT-2026-09" under model "stock.lot"
        And the harvest record includes verified GPS coordinates, laboratory purity data, and harvest timestamp
        When the quality team approves the final GxP release of the lot
        Then the system must compile a SHA-256 organic verification fingerprint hash (生成 SHA-256 有机特征指纹)
        And write the resulting hash alongside its metadata payload to the "agri.blockchain.proof" ledger
        And lock the local lot record from further un-audited modifications
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a completed organic grain harvest lot "GRAIN-LOT-2026-09" under model "stock.lot"',
            'And the harvest record includes verified GPS coordinates, laboratory purity data, and harvest timestamp',
            'When the quality team approves the final GxP release of the lot',
            'Then the system must compile a SHA-256 organic verification fingerprint hash (生成 SHA-256 有机特征指纹)',
            'And write the resulting hash alongside its metadata payload to the "agri.blockchain.proof" ledger',
            'And lock the local lot record from further un-audited modifications'
        ])

    def test_02_blockchain_block_hash_verification(self):
        """
        Scenario: Blockchain Block Hash Verification
        Given a premium organic wine lot "WINE-LOT-CHATEAU-2026" with an active verification record in "agri.blockchain.proof"
        And the proof record contains a transaction hash "0x7f8d9b1a2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f"
        When the compliance auditor requests a blockchain ledger integrity check
        Then the system must query the blockchain node or public ledger endpoint
        And validate that the locally stored transaction hash exactly matches the registered state on the public blockchain (校验链上存证哈希一致性)
        And display a "Verified" status badge with a green compliance signal on the lot passport
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a premium organic wine lot "WINE-LOT-CHATEAU-2026" with an active verification record in "agri.blockchain.proof"',
            'And the proof record contains a transaction hash "0x7f8d9b1a2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f"',
            'When the compliance auditor requests a blockchain ledger integrity check',
            'Then the system must query the blockchain node or public ledger endpoint',
            'And validate that the locally stored transaction hash exactly matches the registered state on the public blockchain (校验链上存证哈希一致性)',
            'And display a "Verified" status badge with a green compliance signal on the lot passport'
        ])

    def test_03_ancestry_chain_proof_validation(self):
        """
        Scenario: Ancestry Chain Proof Validation
        Given a final blended fertilizer lot "FERT-MIX-BATCH-B" with ancestral pedigree links under model "stock.lot"
        And "FERT-MIX-BATCH-B" is composed of parent lots "FERT-RAW-A" and "FERT-RAW-C"
        When the system compiles the comprehensive quality passport and lineage history for "FERT-MIX-BATCH-B"
        Then it must recursively traverse and verify the blockchain proofs of all ancestor lots (递归校验证明链)
        And confirm that no ancestral proof hashes are missing, broken, or mismatched in the "agri.blockchain.proof" registry
        And grant the "Chain of Custody Certified" badge only if all ancestor validations pass
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a final blended fertilizer lot "FERT-MIX-BATCH-B" with ancestral pedigree links under model "stock.lot"',
            'And "FERT-MIX-BATCH-B" is composed of parent lots "FERT-RAW-A" and "FERT-RAW-C"',
            'When the system compiles the comprehensive quality passport and lineage history for "FERT-MIX-BATCH-B"',
            'Then it must recursively traverse and verify the blockchain proofs of all ancestor lots (递归校验证明链)',
            'And confirm that no ancestral proof hashes are missing, broken, or mismatched in the "agri.blockchain.proof" registry',
            'And grant the "Chain of Custody Certified" badge only if all ancestor validations pass'
        ])

    def test_04_tamper_detection_blockchain_validation_failure(self):
        """
        Scenario: Tamper Detection Blockchain Validation Failure
        Given a certified and hashed organic honey lot "HONEY-LOT-GOLDEN" with a registered proof in "agri.blockchain.proof"
        And a local database administrator or rogue script manually alters the "origin_coordinates" field (模拟篡改本地 GPS 数据)
        When the system-wide nightly scheduled data integrity check executes
        Then the system must recalculate the local SHA-256 fingerprint hash
        And detect a mismatch between the newly computed local hash and the immutable hash stored in the "agri.blockchain.proof" record
        And raise an emergency security alert "DATABASE_INTEGRITY_TAMPER_DETECTED" (检测到本地数据篡改，哈希不匹配)
        And flag the honey lot record as "Tainted / Untrusted" in Odoo
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a certified and hashed organic honey lot "HONEY-LOT-GOLDEN" with a registered proof in "agri.blockchain.proof"',
            'And a local database administrator or rogue script manually alters the "origin_coordinates" field (模拟篡改本地 GPS 数据)',
            'When the system-wide nightly scheduled data integrity check executes',
            'Then the system must recalculate the local SHA-256 fingerprint hash',
            'And detect a mismatch between the newly computed local hash and the immutable hash stored in the "agri.blockchain.proof" record',
            'And raise an emergency security alert "DATABASE_INTEGRITY_TAMPER_DETECTED" (检测到本地数据篡改，哈希不匹配)',
            'And flag the honey lot record as "Tainted / Untrusted" in Odoo'
        ])

    def test_05_blockchain_proof_generation_on_transfer(self):
        """
        Scenario: Blockchain Proof Generation on Transfer
        Given a high-value biological breeding stallion "STALLION-PEDIGREE-01" of model "stock.lot"
        And a verified sales transfer order under model "sale.order" ready for shipment
        When the inventory clerk validates the outbound delivery picking "OUT-00125" representing the asset transfer
        Then the system must automatically compile the transfer proof package (Timestamp, Sender, Recipient, Pedigree Hash)
        And generate a new transaction entry in the "agri.blockchain.proof" ledger
        And queue the transfer package for immediate cryptographic block submission to the public blockchain network
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a high-value biological breeding stallion "STALLION-PEDIGREE-01" of model "stock.lot"',
            'And a verified sales transfer order under model "sale.order" ready for shipment',
            'When the inventory clerk validates the outbound delivery picking "OUT-00125" representing the asset transfer',
            'Then the system must automatically compile the transfer proof package (Timestamp, Sender, Recipient, Pedigree Hash)',
            'And generate a new transaction entry in the "agri.blockchain.proof" ledger',
            'And queue the transfer package for immediate cryptographic block submission to the public blockchain network'
        ])

    def test_06_ancestral_tree_transaction_lock_during_proof_compilation(self):
        """
        Scenario: Ancestral Tree Transaction Lock during Proof Compilation
        Given an organic crop lot record under model "stock.lot" (库存批次) with multiple lineage layers
        When the quality auditor initiates the final GxP certification hash compilation (启动存证哈希计算)
        Then the system must execute a cascading SELECT FOR UPDATE to lock the target lot and all its ancestral lot records in the database
        And block other concurrent stock moves under model "stock.picking" (库存调拨) from modifying any record in the lineage chain until the blockchain proof under model "agri.blockchain.proof" (区块链存证) is finalized
        And abort the transaction and raise a ValidationError with code "LINEAGE_RECORD_MUTATED" (溯源物料正在被调拨修改，自动终止哈希计算) if any parent record has been modified during compilation
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given an organic crop lot record under model "stock.lot" (库存批次) with multiple lineage layers',
            'When the quality auditor initiates the final GxP certification hash compilation (启动存证哈希计算)',
            'Then the system must execute a cascading SELECT FOR UPDATE to lock the target lot and all its ancestral lot records in the database',
            'And block other concurrent stock moves under model "stock.picking" (库存调拨) from modifying any record in the lineage chain until the blockchain proof under model "agri.blockchain.proof" (区块链存证) is finalized',
            'And abort the transaction and raise a ValidationError with code "LINEAGE_RECORD_MUTATED" (溯源物料正在被调拨修改，自动终止哈希计算) if any parent record has been modified during compilation'
        ])

    def test_07_dynamic_credit_overdraft_transaction_savepoint_rollback(self):
        """
        Scenario: Dynamic Credit Overdraft Transaction Savepoint Rollback (合作社信用额度穿透事务保存点回滚防呆机制)
        Given a joint clearing balance account inside "account.move" (会计分录模型) with cooperative member status "active" (且合作社成员信用状态为活跃)
        And a dynamic credit limit registered in the virtual ledger (并且在虚拟账簿中登记了固定的动态额度上限)
        When a clearing transaction fails due to concurrent credit overdraft (当清算交易由于信用额度并发穿透导致处理失败时)
        Then the transaction engine must execute rollback to "cr.savepoint" (交易引擎必须强制执行事务回滚到指定的事务保存点)
        And raise a UserError (并且抛出用户错误) with message "CREDIT_OVERDRAFT_TRANSACTION_FAILED" (包含"信用额度超支交易回滚，防范资金坏账"提示信息)
        """
        # Execute BDD Gherkin steps dynamically at runtime on database
        self.execute_gherkin_steps([
            'Given a joint clearing balance account inside "account.move" (会计分录模型) with cooperative member status "active" (且合作社成员信用状态为活跃)',
            'And a dynamic credit limit registered in the virtual ledger (并且在虚拟账簿中登记了固定的动态额度上限)',
            'When a clearing transaction fails due to concurrent credit overdraft (当清算交易由于信用额度并发穿透导致处理失败时)',
            'Then the transaction engine must execute rollback to "cr.savepoint" (交易引擎必须强制执行事务回滚到指定的事务保存点)',
            'And raise a UserError (并且抛出用户错误) with message "CREDIT_OVERDRAFT_TRANSACTION_FAILED" (包含"信用额度超支交易回滚，防范资金坏账"提示信息)'
        ])
