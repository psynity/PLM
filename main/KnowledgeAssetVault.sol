// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract KnowledgeRewardToken is ERC20, Ownable {
    constructor() ERC20("PYCL Knowledge Token", "PYCL-T") Ownable(msg.sender) {}

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }
}

contract KnowledgeAssetVault is Ownable {
    KnowledgeRewardToken public rewardToken;

    struct ResearchNode {
        bytes32 currentHash;
        string projectId;
        uint256 ktiiScore;
        uint256 timestamp;
        bool isVerified;
    }

    mapping(bytes32 => ResearchNode) public ledger;
    mapping(address => uint256) public contributionPoints;

    event KnowledgeAnchored(address indexed researcher, bytes32 indexed nodeHash, string projectId);

    constructor(address _tokenAddress) Ownable(msg.sender) {
        rewardToken = KnowledgeRewardToken(_tokenAddress);
    }

    // Phase 1 & 2 결과물을 온체인에 앵커링하고 보상 집행
    function anchorKnowledge(
        bytes32 _nodeHash, 
        string memory _projectId, 
        int256 _ktiiScore, 
        bytes memory _zkProof // ZKP 증명 패킷 (간략화)
    ) external {
        require(ledger[_nodeHash].timestamp == 0, "Duplicate Hash");

        // 1. 지식 노드 기록
        ledger[_nodeHash] = ResearchNode({
            currentHash: _nodeHash,
            projectId: _projectId,
            ktiiScore: uint256(_ktiiScore > 0 ? _ktiiScore : -_ktiiScore),
            timestamp: block.timestamp,
            isVerified: true
        });

        // 2. KTII 기반 보상 계산 (예시: 기본 10 + |KTII| * 2)
        uint256 rewardAmount = 10 * 10**18 + (uint256(_ktiiScore > 0 ? _ktiiScore : -_ktiiScore) * 2 * 10**18);
        
        // 3. 토큰 지급
        rewardToken.mint(msg.sender, rewardAmount);

        emit KnowledgeAnchored(msg.sender, _nodeHash, _projectId);
    }
}
