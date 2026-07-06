def test_dp_compression(fprime_test_api):
    """Test that data products are compressed by the DpCompression subtopology

    The producer is commanded to request ZLib DEFLATE processing on its data product
    containers. The DataProducts subtopology routes these containers to the
    DpCompression subtopology, which compresses them before they are written to disk.
    """
    # CompressionComplete is a DIAGNOSTIC event, which is filtered out by default
    fprime_test_api.send_and_assert_command(
        "CdhCore.events.SET_EVENT_FILTER", ["DIAGNOSTIC", "ENABLED"]
    )
    try:
        # Request ZLib DEFLATE processing on future data product containers
        fprime_test_api.send_and_assert_command(
            "ExamplesDeployment.dpProducer.SET_PROC_TYPES", ["PROC_TYPE_ZLIB_DEFLATE"]
        )
        fprime_test_api.assert_event(
            "ExamplesDeployment.dpProducer.ProcTypesSet", timeout=5
        )
        # The producer fills a container with 100 records of each type at 10Hz, so
        # allow time for a full container to be produced, compressed, and written
        result = fprime_test_api.await_event(
            "DpCompression.dpCompressProc.CompressionComplete", timeout=30
        )
        assert result, "Data product was not compressed"
        initial_size = result.get_args()[1].val
        final_size = result.get_args()[2].val
        assert final_size < initial_size, "Compression did not reduce the data product size"
        # Verify a data product file is written to disk after compression
        assert fprime_test_api.await_event(
            "DataProducts.dpWriter.FileWritten", timeout=15
        ), "Data product file was not written"
    finally:
        # Restore default processing and event filtering
        fprime_test_api.send_and_assert_command(
            "ExamplesDeployment.dpProducer.SET_PROC_TYPES", ["PROC_TYPE_NONE"]
        )
        fprime_test_api.send_and_assert_command(
            "CdhCore.events.SET_EVENT_FILTER", ["DIAGNOSTIC", "DISABLED"]
        )
