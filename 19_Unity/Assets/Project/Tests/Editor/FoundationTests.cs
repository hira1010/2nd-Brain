using NUnit.Framework;

// ===== Design Reason =====
// Layer: Tests.Editor
// Reason: The foundation smoke test keeps the base test assembly active before feature-specific tests exist.
// Responsibilities:
//   - Verify the EditMode test assembly is discovered.
// =========================
namespace UnityMcpTextbook.Tests.Editor
{
    public sealed class FoundationTests
    {
        [Test]
        public void StepOneFoundation_HasNoGameFeatureRequirement()
        {
            Assert.Pass("Step 1 validates only the project foundation.");
        }
    }
}
